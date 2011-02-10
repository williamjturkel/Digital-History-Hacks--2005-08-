# tenfold-crossvalidation-sample.py
# old bailey
#
# given a list of trials, shuffle and divide
# into ten samples of approximately equal size

import os, random

# if output directory doesn't exist, create it
outdirname = 'Samples_1830s'
if os.path.exists(outdirname) == 0: os.mkdir(outdirname)

# get a list of trials
f = open('trial-ids-1830s.txt', 'r')
triallist = f.readlines()
f.close()

# shuffle it, changing list in place
random.shuffle(triallist)

# do floor division to get basic sample size and remainder
numtrials = len(triallist)
samplesize = numtrials // 10
base = samplesize * 10
remainder = numtrials - base
print "Trials: %d; Base sample: %d; Remainder: %d" % (numtrials, samplesize, remainder)

# get basic samples
sample = {}
for i in range(0,10):
    index = i * samplesize
    offset = index + samplesize
    sample[i] = triallist[index:offset]

# distribute remainder as equally as possible
tailend = range(base, base+remainder)
i = 0
for t in tailend:
    sample[i].append(triallist[t])
    i += 1

# do sanity check
sanity = 0
for k in sample.keys(): sanity += len(sample[k])
if sanity != numtrials:
    print "Sanity check failed"
    quit()

# write samples to files
for k in sample.keys():
    outfilename = outdirname + '\\sample' + str(k) + '.txt'
    f = open(outfilename, 'w')
    for tr in sample[k]: f.write(str(tr))
    f.close()

