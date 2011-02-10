# offence-index.py
# old bailey
#
# given a list mapping trial id to offence, create
# lists of trials that fall into each offence category

import os

infile = open('offence-categories-1830s.txt', 'r')
triallist = infile.readlines();
infile.close()

# get a list of unique offences
alloffences = []
for tr in triallist:
    rowlist = tr.split(',')
    offencelist = rowlist[1:]
    alloffences += map(lambda x: x.strip(), offencelist)

print "Total number of offences: " + str(len(alloffences))
uniqoffences = list(set(alloffences))
print "Number of unique offences: " + str(len(uniqoffences))
# print uniqoffences

# if output directory doesn't exist, create it
outdirname = 'Offences_1830s'
if os.path.exists(outdirname) == 0: os.mkdir(outdirname)

# create empty dictionary structure
offencedict = {}
for u in uniqoffences: offencedict[u] = []

# go through file again, this time adding each trial to
# dictionary of offences

for tr in triallist:
    rowlist = tr.split(',')
    trialid = rowlist[0]
    # need to get rid of trailing newlines
    fulloffencelist = map(lambda x: x.strip(), rowlist[1:])
    # can be charged with multiple counts of same offence
    offencelist = list(set(fulloffencelist))
    # update dictionary
    map(lambda x: offencedict[x].append(trialid), offencelist)

# write out each dictionary entry as a separate file

for k in offencedict.keys():
    outfilename = outdirname + '\\' + k + '.txt'
    outfile = open(outfilename, 'w')
    for tr in offencedict[k]: outfile.write(tr+'\n')
    outfile.close()