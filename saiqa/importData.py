import csv
import re
import numpy as np

reader = ""

def octalConv(x):
    ans = []
    for line in x:
        number = ord(line)
        convNum = oct(number)
        convNum = int(convNum[2:])
        
        ans.append(convNum)
    return ans

def reformatAr(x):
    data = []
    for line in x:
        ex = line.split(',')
        for i in range(len(ex)):
            ex[i] = int(ex[i])
        data.append(ex)
    return data

def expandArray(x):
    full = []
    hold = []
    corr = []
    
    for lines in x:
        #print(lines)
        hold = lines.split(',')
        for line in hold:
            corr.append(int(line))
        full.append(corr)
    return full

def wideArray(x, weight):
    #wide = np.zeros([weight.shape[1],len(np.unique(oneHotTrain))])
    wide = np.zeros([5908,])
    for i in range(0,len(x)):
        wide[i] = x[i]
    return wide

def shrinkArray(x,l):
    print(x)
    small = np.zeros([l,])
    for i in range(0,len(x)):
        small[i] = x[i]
    return small

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

def probsToWord(x):
    #print(x)
    if x[0] == 1:
        return 'time'
    elif x[1] == 1:
        return 'location'
    elif x[2] == 1:
        return 'property'
    elif x[3] == 1:
        return 'possession'

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
    print(len(data))
    data = expandArray(data)
    reader.close()
    return np.array(data)

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
