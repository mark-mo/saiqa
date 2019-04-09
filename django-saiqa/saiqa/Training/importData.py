# Holds helper methods for the implementation of a softmax regression
# Created by Mark Mott
import csv
import re
import numpy as np
import string

reader = ""

# Converts octal decimal to its corresponding category
def probsToWord(prob):
    if int(prob[0]) == 1:
        return 'time'
    elif int(prob[1]) == 1:
        return 'location'
    elif int(prob[2]) == 1:
        return 'property'
    elif int(prob[3]) == 1:
        return 'possession'
    else:
        return 'property'

# Converts character into octal decimal
def octalConv(x):
    ans = []
    for line in x:
        number = ord(line)
        convNum = oct(number)
        convNum = int(convNum[2:])
        
        ans.append(convNum)
    return ans

# Fixes a 2d array to account for bug in Numpy
def reformatAr(x):
    data = []
    for line in x:
        ex = line.split(',')
        for i in range(len(ex)):
            ex[i] = int(ex[i])
        data.append(ex)
    return data

# Fixes a 1D array to account for bug in Numpy
def reformatSingAr(x):
    data = []
    ex = x.split(',')
    for line in ex:
        data.append(int(line))
    return data

# Deprecated: Use reformatAr/reformatSingAr instead
def expandArray(x):
    full = []
    hold = []
    corr = []
    
    for lines in x:
        hold = lines.split(',')
        for line in hold:
            corr.append(int(line))
        full.append(corr)
    return full

# Adjusts size of array to allow for matrix multiplication
def wideArray(x, weight):
    high = 0
    for line in x:
        if len(line) > high:
            high = len(line)
    wide = np.zeros([len(x),len(weight)])
    for i in range(0,len(x)):
        for j in range(0,len(x[i])):
            wide[i][j] = x[i][j]
    return wide

# Adjusts size of a 2-d array to allow for matrix multiplication
def wideSingleArray(x, weight):
    wide = np.zeros([len(weight)])
    if len(x) > len(weight):
        for i in range(0, len(weight)):
            wide[i] = x[i]
    else:
        for i in range(0, len(x)):
            wide[i] = x[i]
    np.asarray(wide)
    return wide

# Reformats input array into int32
def format32(x):
    data = np.empty_like(x)
    i = 0 # Row
    j = 0 # Column
    for lines in x:
        j = 0
        for line in lines:
            data[i,j] = int(x[i,j])
            j = j + 1
        i = i + 1
    return data

# Retrieve all training sentences. Not used in favor of getTraining and getTesting
def getAll():
    placeHolder = 0
    trainArr=[]
    reader = open('focusWords.txt','r')
    rawread = open('exec.txt','r')
    data = []
    raw = []
    for point in reader:
        point = re.sub('\\n','',point)
        data.append(point)
    for point in rawread:
        point = re.sub('\\n','',point)
        raw.append(point)
    return np.array(data), np.array(raw)

# Gets sentences to train off of based on the amount specified
def getTraining(amount):
    placeHolder = 0
    trainArr=[]
    reader = open('focusWords.txt','r')
    data = []
    for point in reader:
        if placeHolder < amount:
            point = re.sub('\\n','',point)
            data.append(point)
        elif placeHolder >= amount:
            data = expandArray(data)
            reader.close()
            return np.array(data), placeHolder
        placeHolder = placeHolder + 1

# Gets sentences to test off of based on the amount specified
def getTesting(amount, placeHolder):
    data = []
    count = 0
    reader = open('focusWords.txt','r')
    for row in reader:
        if count >= placeHolder:
            if count < amount + placeHolder:
                row = re.sub('\\n','',row)
                data.append(row)
        count = count + 1
    data = expandArray(data)
    reader.close()
    return np.array(data)

# Gets answers to sentences of based on the amount and starting point specified
def getOneHot(amount, start):
    trainArr=[]
    datafile = open('oneHot.csv','r')
    reader = csv.reader(datafile, delimiter='\n')
    data = []
    count = 0
    for row in reader:
        if count > start:
            if count < (start + amount):
                data.append(row[0])
        count = count + 1
    datafile.close()
    full = np.array(data)
    return full
