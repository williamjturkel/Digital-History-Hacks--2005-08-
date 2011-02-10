# clean-copy-trials.py
# old bailey
#
# given a directory of trial files each marked with XML
# create a parallel directory of files with all tagging stripped

import os, sys, re

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# given a string containing XML, remove all characters
# between matching pairs of angled brackets, inclusive
def stripTags(xml):
    inside = 0
    text = ''
    for char in xml:
        if char == '&lt;':
            inside = 1
            continue
        elif (inside == 1 and char == '&gt;'):
            inside = 0
            continue
        elif inside == 1:
            continue
        else:
            text += char
    return text
	
# given a local copy of an XML file, return string
# of lowercase text from page
def localXMLFileToText(xmlfile):    
    f = open(xmlfile, 'r')
    xml = f.read()
    f.close()
    text = stripTags(xml).replace('&nbsp;', ' ')
    text = text.replace('&#x2014;', ' ')
    text = text.replace('&#x22;', '')
    return text.lower()
	
# given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric)
def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)
	
# get a list of trial files to process
indirname = 'Mined_1830s'
filelist = getFileNames(indirname)

# if output directory doesn't exist, create it
outdirname = 'Mined_1830s_clean'
if os.path.exists(outdirname) == 0: os.mkdir(outdirname)

# page images have 12-digit number
imgpattern = re.compile(r'\d{12}', re.UNICODE)

for fn in filelist:

    # provide feedback for user
    print 'Processing ' + fn
    sys.stdout.flush()
    
    # read XML file into string and remove formatting
    infile = indirname + '\\' + fn
    instr = localXMLFileToText(infile)
    instr = imgpattern.sub(' ', instr)
    wordlist = stripNonAlphaNum(instr)
    
    # output clean lowercase alphanumeric text
    outfile = outdirname + '\\' + 'clean_' + fn
    f = open(outfile, 'w')
    for w in wordlist: f.write(w+' ')
    f.close()

