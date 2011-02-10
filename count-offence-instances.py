# count-offence-instances.py
# old bailey
#
# given a crossvalidation sample, count the
# number of offence instances in each partition

import os

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist
	
# get list of matching trials
offencedir = 'Offences_1830s'
offencefile = 'theft-simplelarceny.txt'
f = open(offencedir + '\\' + offencefile, 'r')
triallist = f.readlines()
f.close()

# get a list of sample files to process
indirname = 'Samples_1830s'
samplelist = getFileNames(indirname)

# count instances
instancetotal = 0
for s in samplelist:
    instances = 0
    f = open(indirname + '\\' + s, 'r')
    samptriallist = f.readlines()
    f.close()
    for tr in samptriallist:
        if tr in triallist: instances += 1
    print "%s: %d" % (s, instances)
    instancetotal += instances
    
# sanity check
print "Number of offences: %d" % len(triallist)
print "Sum of offences: %d" % instancetotal

