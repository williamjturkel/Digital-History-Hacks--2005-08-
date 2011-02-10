# cross-validate-tfidf-learner.py
# old bailey
#
# test performance of TF/IDF based learner on a
# cross-validation sample

import os, string, re, sys
from bayesian import *

# the routine to extract features has to be bypassed
# this expects a string made by concatenating terms
# with highest TF/IDF
def passtfidf(doc):
    wordlist = doc.split(' ')
    return dict([(w,1) for w in wordlist])

# set learner type and number of features
learner = 'tfidf'
numfeatures = 50

# read the 10 sample files into an array of lists of the form
# samplelist[sample_number][item_number]
sampledir = 'Samples_1840s'
samplelist = []
for i in range(0, 10):
    f = open(sampledir + '\\' + 'sample' + str(i) + '.txt', 'r')
    sample = []
    sample = f.readlines()
    sample = [x.rstrip() for x in sample]
    samplelist.append(sample) 
    f.close

# offence being tested
offencedir = 'Offences_1840s'
offencefile = 'theft-simplelarceny.txt'
f = open(offencedir + '\\' + offencefile, 'r')
offencelist = f.readlines()
offencelist = [x.rstrip() for x in offencelist]
f.close()
offencecount = len(offencelist)

# trials
trialdir = 'TFIDF_1840s'

# open output file and write the file header
outfile = 'cross-val-tfidf-lrn.txt'
f = open(outfile, 'w')
f.write('OLD BAILEY Tenfold Cross-Validation Learning Run\n\n')
f.write('Offence: ' + offencedir + '\\' + offencefile + '\n')
f.write('Learning run: tfidf, ' + str(numfeatures) + ' features\n')
f.write("\nRun, %7s, %7s, %7s, %7s\n" % ('Hit', 'Miss', 'FalseP', 'CorrN'))

# run tests
cl = []
for i in range(0,3):
    
    # train a new learner for each run
    cl.append(naivebayes(passtfidf))
    
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
    print str(i) + ' Training'
    sys.stdout.flush()

    for r in trainingsample:
        trialstr = ''
        ff = open(trialdir + '\\tfidf_' + r, 'r')
        whole = ff.readlines()
        feat = min(len(whole)-1, numfeatures)
        for k in range(0, feat):
            linein = whole[k].split(',')
            trialstr += str(linein[0])
            trialstr += ' '
        ff.close()

        if r in offencelist:
            # print trialstr.rstrip()
            cl[i].train(trialstr.rstrip(),'y')
        else:
            # print trialstr.rstrip()
            cl[i].train(trialstr.rstrip(),'n')
    
    # test the learner on testing sample
    print str(i) + ' Testing'
    sys.stdout.flush()
        
    for t in testingsample:
        
        # read trial into string
        trialstr = ''
        ff = open(trialdir + '\\tfidf_' + t, 'r')
        whole = ff.readlines()
        feat = min(len(whole)-1, numfeatures)
        for k in range(0, feat):
            linein = whole[k].split(',')
            trialstr += str(linein[0])
            trialstr += ' '
        ff.close()
    
        # use learner to categorize trial
        g = cl[i].classify(trialstr.rstrip(),default='n')

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