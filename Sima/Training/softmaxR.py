# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# Code from https://gist.github.com/awjuliani/5ce098b4b76244b7a9e3#file-softmax-ipynb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import sys
import time as ti

import argparse

# Get training data from mnist
import importData as id

gradArr = []
w = []

# Gets data from importdata
def getData():
    # Allows train and test arrays to be the same size
    total,place = id.getTraining(150)
    train = total[:140]
    test = total[140:150]
    oneHotTotal = id.getOneHot(151,0)
    oneHotTrain = oneHotTotal[:140]
    oneHotTest = oneHotTotal[140:150]
    return train,test,oneHotTrain,oneHotTest

# Creates an array of only 1 or 0
def toSparse(x):
    index = 0
    large = 0
    # Find index of largest number
    for i in range(0,len(x)):
        if x[i] > large:
            large = x[i]
            index = i
    
    # Modify array
    for i in range(0,len(x)):
        if x[i] == large:
            x[i] = 1
        else:
            x[i] = 0
    return x

# Transposes matrices
def tranSin(x):
    size = len(x)
    rez = np.zeros((size,1))
    
    # For 1D arrays
    if type(x[0]) == type(np.float64(5.9975)):
        for i in range(0,size):
            rez[i][0] = x[i]
    # For 2D arrays
    else:
        sizeIn = len(x[0])
        rez = np.zeros((sizeIn,size))
        for i in range(0,size):
            for j in range(0,sizeIn):
                rez[j][i] = x[i][j]
    return rez

# Correctly formats the one-hot matrix
def oneHotIt(Y):
    line = id.reformatSingAr(Y)
    line = np.asarray(line)
    m = line.shape[0]
    OHX = scipy.sparse.csr_matrix((np.ones(m), (line, np.array(range(m)))))
    OHX = np.array(OHX.todense()).T
    return OHX

# Calculates the current loss of the softmax cost function
def lossFunc(w,m,x,y_mat,lam,prob):
    yProb = prob.dot(y_mat)
    sumY = np.sum(yProb)
    left = np.dot((-1 / m),sumY)
    weightMul = np.square(w)
    lam = lam/2
    right = np.dot(np.sum(weightMul),lam)
    full = left + right
    return full

# Modifies array to allow for matrix calculations
def expandAr(x,shape): # Expand matrix by 1
    shape = len(x)
    sizeIn = len([0]) + 1
    xT = np.resize(x,(shape, sizeIn))
    for i in range(len(xT)):
        xT[i][1] = 0
    return xT

# Calculates the gradient
def gradFunc(w,m,x,y_mat,lam,prob):
    #grad = (-1 / m) * np.dot(tranSin(x),(y_mat - prob)) + lam*w
    probT = tranSin(prob)
    probT = expandAr(probT,probT.shape)
    
    yProb = np.subtract(probT,y_mat)
    xTr = tranSin(x)
    xTr = expandAr(xTr,xTr.shape)
    dotM = np.dot(xTr,tranSin(yProb))
    full = (-1 / m) * dotM + lam*w
    return full

# Gets the current gradient and loss of the softmax cost function
def getGrad(w,x,y_mat,lam):
    x = np.asarray(x,'float64')
    m = x.shape[0] #First we get the number of training examples
    scores = np.dot(x,w) #Then we compute raw class scores given our input and current weights
    y_mat = oneHotIt(y_mat) # Create a One-Hot matrix from answers
    prob = softmax(scores) #Next we perform a softmax on these scores to get their probabilities
    loss = lossFunc(w,m,x,y_mat,lam,prob)
    grad = gradFunc(w,m,x,y_mat,lam,prob) #And compute the gradient for that loss
    gradArr.append(loss)
    return grad,loss

# Actual softmax regression code
def softmax(z):
    z -= np.max(z) # subtract the max for numerical stability
    expZ = np.exp(z)
    trExp = tranSin(expZ)
    bottom = trExp / np.sum(np.exp(z))
    sm = tranSin(bottom) # Run the softmax function and transpose the matrixes
    return sm

# Returns answer of someX being run through softmax
def getProbs(someX):
    probs = softmax(np.dot(someX,w))
    return probs

# Code that will actually be implemented to categorize a single sentence
def response(x):
    w = np.loadtxt("weights\softweights.csv",delimiter=",")
    someX = id.octalConv(x)
    someX = id.wideArray(someX,w)
    
    probs = softmax(np.dot(someX,w))
    return id.probsToWord(probs)

# Returns how accurate the weights make the softmax regression
def getAccuracy(someX,someY,w):
    totalCorrect = 0
    prob = getProbs(someX)
    someY = id.reformatAr(someY)
    someY = np.asarray(someY, 'float64')
    for i in range(len(someX)):
        prede = toSparse(prob[i])
        if np.array_equal(prede, someY[i]):
            totalCorrect = totalCorrect + 1
    accuracy = totalCorrect/(float(len(someY))) # Calculates how many times the predicted output equals the expected output
    return accuracy

# Main/starting method
def mainRun():
    global w
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--restore", help="restore previously trained weights (default=false)")
    args = parser.parse_args()
    
    train,test,oneHotTrain, oneHotTest = getData()
    
    w = np.random.random_integers(4, size=(train.shape[1],len(np.unique(oneHotTrain))))
    if args.restore:
        # Restores weights if the tag is present
        w = np.loadtxt("weights\softweights.csv",delimiter=",")
    
    # Formats train and test to be the correct size
    train = id.wideArray(train,w)
    test = id.wideArray(test,w)
    
    # Hyperparameters
    lam = 1
    iterations = 2000
    learningRate = 1e-4
    # Extra variables
    count = 0
    pastMean = 0
    for i in range(0,iterations):
        for time in train:
            grad,loss = getGrad(w,time,oneHotTrain[count],lam)
            w = w - (learningRate * grad) # Modify weights based on gradient
            # Output progress to console
            sys.stdout.write("\r {} / {} : lower = {}, slope = {}".format(i, iterations,(np.mean(gradArr)-pastMean), (1/(np.mean(gradArr)-pastMean))))
            pastMean = np.mean(gradArr)
            sys.stdout.flush()
            count = count + 1 # Increment count by one
        count = 0
    # Get accuracy
    print('Training Accuracy: ' + str(getAccuracy(train,oneHotTrain,w)))
    print('Testing Accuracy: ' + str(getAccuracy(test,oneHotTest,w)))
    # Save weights to a csv file for future use
    np.savetxt("weights\softweights.csv",w,delimiter=",")

# Allows the code to run
mainRun()