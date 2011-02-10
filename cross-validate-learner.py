# cross-validate-learner.py
# old bailey
#
# test performance of learner on a
# cross-validation sample

import os, string, re, sys
from bayesian import *

# set learner type to 'coinflip', 'getwords', 'gettwograms', 'tfidfngrams'
learner = 'tfidfngrams'

# read the 10 sample files into an array of lists of the form
# samplelist[sample_number][item_number]
sampledir = 'Samples_1830s'
samplelist = []
for i in range(0, 10):
    f = open(sampledir + '\\' + 'sample' + str(i) + '.txt', 'r')
    sample = []
    sample = f.readlines()
    sample = [x.rstrip() for x in sample]
    samplelist.append(sample) 
    f.close

# offence being tested
offencedir = 'Offences_1830s'
offencefile = 'theft-simplelarceny.txt'
f = open(offencedir + '\\' + offencefile, 'r')
offencelist = f.readlines()
offencelist = [x.rstrip() for x in offencelist]
f.close()
offencecount = len(offencelist)

# trials
trialdir = 'Mined_1830s_clean'

# open output file and write the file header
outfile = 'cross-val-learn.txt'
f = open(outfile, 'w')
f.write('OLD BAILEY Tenfold Cross-Validation Learning Run\n\n')
f.write('Offence: ' + offencedir + '\\' + offencefile + '\n')
if learner == 'coinflip':
    f.write('Learning run: coinflip\n')
elif learner == 'getwords':
    f.write('Learning run: getwords\n')
elif learner == 'gettwograms':
    f.write('Learning run: gettwograms\n')
else:
    f.write('Learning run: tfidfngrams\n')
f.write("\nRun, %7s, %7s, %7s, %7s\n" % ('Hit', 'Miss', 'FalseP', 'CorrN'))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cl = []
for i in range(0, 1):
    
    # train a new learner of the appropriate kind for each run
    if learner == 'getwords':
        cl.append(naivebayes(getwords))
    elif learner == 'gettwograms':
        cl.append(naivebayes(gettwograms))
    elif learner == 'tfidfngrams':
        cl.append(naivebayes(gettfidfngrams))
    else:
        cl.append('coinflip')

    # response categories
    hits = 0
    misses = 0
    falseps = 0
    corrns = 0
        
    # set testing sample to i
    print str(i) + ' Loading samples...'
    testingsample = []
    testingsample = samplelist[i]
    
    # set training sample to the concatenation of the others
    trainingsample = []
    for j in range(0, i): trainingsample.extend(samplelist[j])
    for j in range((i+1), 10): trainingsample.extend(samplelist[j])
                    
    # train the learner on training sample
    if learner != 'coinflip':
    
        print str(i) + ' Training'
        sys.stdout.flush()

        for r in trainingsample:
            trialstr = ''
            if learner != 'tfidfngrams':
                trialstr = open(trialdir + '\\clean_' + r, 'r').read()
            else:
                trialstr = open('TFIDF15_2gram_1830s\\tfidf15_2gram_' + r, 'r').read()
                print "training"
                print trialstr[0:40]
            if r in offencelist: cl[i].train(trialstr,'y')
            else: cl[i].train(trialstr,'n')
    
    # test the learner on testing sample
    print str(i) + ' Testing'
    sys.stdout.flush()
        
    for t in testingsample:
        
        # read trial into string
        trialstr = ''
        if learner != 'tfidfngrams':
            trialstr = open(trialdir + '\\clean_' + t, 'r').read()
        else:
            trialstr = open ('TFIDF15_2gram_1830s\\tfidf15_2gram_' + t, 'r').read()
            print "testing"
            print trialstr[0:40]
    
        # use learner to categorize trial
        if learner == 'coinflip':
            g = coinflip()
        else:
            g = cl[i].classify(trialstr,default='n')

        # compare categorization with actual category
        if t in offencelist:
            # hit or miss
            if g == 'y': hits+=1
            else: misses+=1
        else:
            # false positive or correct negative
            if g == 'y': falseps+=1
            else: corrns+=1

    # write out learner performance
    f.write("%03d, %07d, %07d, %07d, %07d\n" % (i, hits, misses, falseps, corrns))
    f.flush()
    
print 'Done'
sys.stdout.flush()
    
# close output file
f.close()