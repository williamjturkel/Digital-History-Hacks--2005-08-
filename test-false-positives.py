# test-false-positives.py
# old bailey
#
# given results from online run, returns
# categories of all false positives

import os, string, re, sys

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# given a trial file name, return long integer
# that can be used for sorting
def trialtoint(trialname):
    pattern = re.compile(r'(\d{8})-(\d+)', re.UNICODE)
    match = pattern.search(trialname)
    date = match.group(1)
    id = match.group(2)
    return long("%8d%06d" % (long(date), long(id)))

# list of result files to test
resultdir = 'Online_Runs_1830s'
resultfilelist = getFileNames(resultdir)

# file of offence categories
categoriesfile = 'offence-categories-1830s.txt'

# output directory
outdir = 'Online_FPs_1830s'
if os.path.exists(outdir) == 0: os.mkdir(outdir)

for resultfile in resultfilelist:
    
    outfile = outdir + '\\fps-tfidf50-' + resultfile
    g = open(outfile, 'w')
    g.write('OLD BAILEY False Positives\n\n')
    g.write('Offence: ' + resultfile + '\n\n')

    # create a dictionary mapping trial to offence(s)
    f = open(categoriesfile, 'r')
    triallist = f.readlines()
    f.close()
    offencecats = {}
    for t in triallist:
        linein = t.split(',')
        trstr = str(trialtoint(linein[0]))
        offencecats[trstr] = []
        for l in linein[1:]:
            offencecats[trstr].append(l.rstrip())
    
    # find the false positives and compile a dictionary of offence counts
    f = open(resultdir + '\\' + resultfile, 'r')
    resultlist = f.readlines()
    f.close()
    pattern = re.compile(r'(\d{14})(,\s+\d{6},\s+)(y,\s+n,)', re.UNICODE)
    offencecounts = {}
    for r in resultlist:    
        match = pattern.search(r)
        if match:
            trialint = match.group(1)
            for o in offencecats[trialint]:
                if offencecounts.has_key(o):
                    offencecounts[o] += 1
                else:
                    offencecounts[o] = 1
                    
    # output offence counts
    for key in offencecounts:
        g.write(key + ", " + str(offencecounts[key]) + '\n')
        
    g.close()
