#Converts a text file into octal decimal
import re

lines = []
conLines=[]
count = 0

fo = open('C:\\Users\\Mark\\Desktop\\Python_Scripts\\datasetSent\\out.txt', "r")
# Cleans and moves contents of out.txt into lines
with fo as file:
    for line in file:
        line= line.strip()
        lines.append(line)
        print(str(count) + ': ' + line)
        count = count + 1

wordCount = 0
totalCount = 0;
ident = ''
totalIdent = ''
convNum = 0

# Converts words into octal decial
for line in lines:
    #words = line.split()
    for word in line:
        while wordCount < len(word):
            number = ord(word[wordCount])
            convNum = oct(number)
            convNum = convNum[2:]
            ident += str(convNum)
    
            wordCount+=1
        wordCount=0
        totalIdent += convNum + ','
        ident = ''
    #print(totalIdent)
    conLines.append(totalIdent)
    totalIdent = ''
    totalCount += 1
fo.close()
    
# Output result
#fi = open('C:\\Users\\Mark\\Desktop\\Python_Scripts\\datasetSent\\focusWords.txt', "w")
for line in hold:
    #fi.write(line+'\n')
    print(line)

#fi.close()