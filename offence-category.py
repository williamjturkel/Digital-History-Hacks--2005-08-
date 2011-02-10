# offence-category.py
# old bailey
#
# given a directory of trial files each marked with XML
# extract a list mapping trial id to offence

import os, sys, re
from BeautifulSoup import BeautifulStoneSoup

# given a directory string, return a list of file names
def getFileNames(dirstr):
    import os
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# given an XML tag describing an offence, return as a
# standardized string
def standardizeOffenceTags(offstring):
    stdstr = offstring.replace('<', '')
    stdstr = stdstr.replace('>', '')
    stdstr = stdstr.replace('\"', '')
    stdstr = stdstr.replace('category=', '')
    stdstr = stdstr.replace(' ', '-')
    return stdstr.lower()
	
# get a list of trial files to process
indirname = 'Mined_1830s'
filelist = getFileNames(indirname)

# scrape out the first child node of each offence
offencepattern = re.compile(r'<.*?>', re.UNICODE)

resultsfile = open('offence-categories-1830s.txt', 'w')

for fn in filelist:

    outstr = fn
    
    # read XML file into string and parse it
    f = open(indirname+'\\'+fn, 'r')
    fnxml = f.read()
    f.close()
    fnsoup = BeautifulStoneSoup(fnxml)
    offencelist = fnsoup.findAll('offence')
    
    # extract offences
    for o in offencelist:
        offence = o.contents[0]
        # one trial had a blank space in front of first node
        if offence == ' ': offence = o.contents[1]
        omatch = offencepattern.match(str(offence))
        offstr = omatch.group()
        outstr += ',' + standardizeOffenceTags(offstr)

    # write offence data to file
    resultsfile.write(outstr+'\n')
    resultsfile.flush()

    # provide feedback for user
    print outstr
    sys.stdout.flush()

resultsfile.close()

