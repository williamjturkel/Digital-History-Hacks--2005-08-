# trial-id-list.py
# old bailey
#
# create a list of trial ids

import os

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# get a list of trial files
indirname = 'Mined_1830s'
triallist = getFileNames(indirname)

# write it out
resultsfile = open('trial-ids-1830s.txt', 'w')
for tr in triallist:
    resultstr = tr + '\n'
    resultsfile.write(resultstr)
    
resultsfile.close()

