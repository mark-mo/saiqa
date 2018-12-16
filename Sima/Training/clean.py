# Handles separating input from out.txt into  sentences
import re
datafile = open('out.txt', 'r')

hold = []
final = []

for line in datafile:
    if len(line) > 3:
        #s = re.sub('\[.*?\]|\(.*?\)|\s*$|\.$','',line)
        s = re.sub('\d+: ','',line)
        hold.append(s)
    #s = re.split('(?<![A-Z]\w)\. |\.\n')
        
for line in hold:
    if len(line) > 3:
        #s = re.sub('\[.*?\]|\(.*?\)|\s*$|\.$','',line)
        #s = re.sub('\d+: ','',line)
        s = re.split('(?<![A-Z]\w)\. |\.\n',line)
        final.append(s)
        
for line in hold:
    print(line,end='')