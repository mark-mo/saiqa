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
import scipy.sparse
import sys
import argparse
import os
import saiqa.Training.importData as id

gradArr = []
w = []


def getData():
    # Allows train and test arrays to be the same size
    total, place = id.getTraining(800)
    train = total[:760]
    test = total[760:800]
    oneHotTotal = id.getOneHot(801, 0)
    oneHotTrain = oneHotTotal[:760]
    oneHotTest = oneHotTotal[760:800]
    return train, test, oneHotTrain, oneHotTest


# Creates an array of only 1 or 0
def toSparse(x):
    index = 0
    large = 0
    focus = x[0]
    # Find index of largest number
    index = np.argmin(focus)
    large = focus[0]

    # Modify array
    for i in range(0, len(focus)):
        if focus[i] == large:
            focus[i] = 1
        else:
            focus[i] = 0
    return focus


def tranSin(x):
    size = len(x)
    rez = np.zeros((size, 1))

    if type(x[0]) == type(np.float64(5.9975)):
        for i in range(0, size):
            rez[i][0] = x[i]
    else:
        sizeIn = len(x[0])
        rez = np.zeros((sizeIn, size))
        for i in range(0, size):
            for j in range(0, sizeIn):
                rez[j][i] = x[i][j]
    return rez


def oneHotIt(Y):
    line = id.reformatSingAr(Y)
    line = np.asarray(line)
    m = line.shape[0]
    OHX = scipy.sparse.csr_matrix((np.ones(m), (line, np.array(range(m)))))
    OHX = np.array(OHX.todense()).T
    return OHX


def lossFunc(w, m, x, y_mat, lam, prob):
    yProb = prob.dot(y_mat)
    sumY = np.sum(yProb)
    left = np.dot((-1 / m), sumY)
    weightMul = np.square(w)
    lam = lam / 2
    right = np.dot(np.sum(weightMul), lam)
    full = left + right
    return full


def expandAr(x, shape):  # Expand matrix by 1
    shape = len(x)
    sizeIn = len([0]) + 1
    xT = np.resize(x, (shape, sizeIn))
    for i in range(len(xT)):
        xT[i][1] = 0
    return xT


def gradFunc(w, m, x, y_mat, lam, prob):
    # grad = (-1 / m) * np.dot(tranSin(x),(y_mat - prob)) + lam*w
    probT = tranSin(prob)
    probT = expandAr(probT, probT.shape)

    yProb = np.subtract(probT, y_mat)
    xTr = tranSin(x)
    xTr = expandAr(xTr, xTr.shape)
    dotM = np.dot(xTr, tranSin(yProb))
    full = (-1 / m) * dotM + lam * w
    return full


def getGrad(w, x, y_mat, lam):
    x = np.asarray(x, 'float64')
    m = x.shape[0]  # First we get the number of training examples
    scores = np.dot(x, w)  # Then we compute raw class scores given our input and current weights
    y_mat = oneHotIt(y_mat)  # Create a One-Hot matrix from answers
    prob = softmax(scores)  # Next we perform a softmax on these scores to get their probabilities
    loss = lossFunc(w, m, x, y_mat, lam, prob)
    grad = gradFunc(w, m, x, y_mat, lam, prob)  # And compute the gradient for that loss
    gradArr.append(loss)
    return grad, loss


def softmax(z):
    z -= np.max(z)  # subtract the max for numerical stability
    expZ = np.exp(z)
    trExp = tranSin(expZ)
    bottom = trExp / np.sum(np.exp(z))
    sm = tranSin(bottom)  # Run the softmax function and transpose the matrixes
    return sm


def getProbs(someX):
    probs = softmax(np.dot(someX, w))
    return probs


def response(x):
    wpath = os.getcwd() + "\saidj\weights\softweights.csv"
    w = np.loadtxt(wpath, delimiter=",")
    someX = id.octalConv(x)
    someX = id.wideSingleArray(someX, w)
    scores = np.dot(someX, w)

    probs = softmax(scores)
    word = toSparse(probs)
    return id.probsToWord(word)


def getAccuracy(someX, someY, w):
    totalCorrect = 0
    prob = getProbs(someX)
    someY = id.reformatAr(someY)
    someY = np.asarray(someY, 'float64')
    for i in range(len(someX)):
        prede = toSparse(prob[i])
    entry = someY[i]
    if np.array_equal(prede, entry):
        totalCorrect = totalCorrect + 1
    else:
        print('false')
    accuracy = totalCorrect / (float(len(someY)))  # Calculates how many times the predicted output equals the expected output
    return accuracy


def mainRun():
    global w
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--restore", help="restore previously trained weights (default=false)")
    args = parser.parse_args()

    train, test, oneHotTrain, oneHotTest = getData()

    w = np.random.random_integers(4, size=(train.shape[1], len(np.unique(oneHotTrain))))
    if args.restore:
        w = np.loadtxt("weights\softweights.csv", delimiter=",")

    train = id.wideArray(train, w)
    test = id.wideArray(test, w)

    lam = 1
    iterations = 2000
    learningRate = 1e-4
    count = 0
    pastMean = 0
    for i in range(0, iterations):
        for time in train:
            grad, loss = getGrad(w, time, oneHotTrain[count], lam)
            w = w - (learningRate * grad)
            sys.stdout.write("\r {} / {} : lower = {}, slope = {}".format(i, iterations, (np.mean(gradArr) - pastMean),
                                                                          (1 / (np.mean(gradArr) - pastMean))))
            pastMean = np.mean(gradArr)
            sys.stdout.flush()
            count = count + 1
        count = 0
    print('Training Accuracy: ' + str(getAccuracy(train, oneHotTrain, w)))
    print('Testing Accuracy: ' + str(getAccuracy(test, oneHotTest, w)))
    np.savetxt("weights\softweights.csv", w, delimiter=",")
