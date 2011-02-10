# split-into-trials.py
# old bailey
#
# split each of the tagged XML files into separate trial files

import os, sys, re
from BeautifulSoup import BeautifulStoneSoup

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# get a list of XML files to process
indirname = 'Tagged_final\Tagged_1830s_Files'
filelist = getFileNames(indirname)

# if output directory doesn't exist, create it
outdirname = 'Mined_1830s'
if os.path.exists(outdirname) == 0: os.mkdir(outdirname)

# extract each trial from each XML file and save it separately
for fn in filelist:

    # provide feedback for user
    print 'Processing ' + fn
    sys.stdout.flush()
    
    # read XML file into string and parse it
    f = open(indirname+'\\'+fn, 'r')
    fnxml = f.read()
    f.close()
    fnsoup = BeautifulStoneSoup(fnxml)
    triallist = fnsoup.findAll('trial')
    
    # extract trial id and use as filename for each trial
    trialpattern = re.compile(r'id=\"(t-\d+-\d+)', re.UNICODE)
    for tr in triallist:
        matchid = trialpattern.search(str(tr))
        outfilename = outdirname + '\\' + matchid.group(1) + '.txt'
        f = open(outfilename, 'w')
        f.write(str(tr))
        f.close()

