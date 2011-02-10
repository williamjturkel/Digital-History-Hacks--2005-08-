# count-offences.py
# old bailey
#
# using the offence files, quickly count how many
# offences of each type

import os

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# open an output file
resultsfile = open('offence-counts-1830s.txt', 'w')

# get a list of offence files to process
indirname = 'Offences_1830s'
ofilelist = getFileNames(indirname)

# process each file
for ofile in ofilelist:
    
    # get a list of trials for each offence
    f = open(indirname+'\\'+ofile, 'r')
    triallist = f.readlines()
    f.close()
    
    # write results
    resultstr = ofile + '|' + str(len(triallist)) + '\n'
    resultsfile.write(resultstr)

resultsfile.close()

