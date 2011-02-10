# get-date-range.py
# old bailey
#
# given a directory of trial files, return
# an ordered list of trial dates

import os
import re

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# get a list of trial files to process
indirname = 'Mined_1830s'
triallist = getFileNames(indirname)

# strip date out of pre- and post-fixed material
datedict = {}
datepattern = re.compile(r'\d{8}', re.UNICODE)
for tr in triallist:
    matchdate = datepattern.search(tr)
    datedict[matchdate.group()] = '1'

# output file consisting of list of dates    
keys = datedict.keys()
keys.sort()
outfilename = 'dates-1830s.txt'
f = open(outfilename, 'w')
for k in keys: f.write(str(k)+'\n')
f.close()

