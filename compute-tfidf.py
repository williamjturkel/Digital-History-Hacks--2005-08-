# compute-tfidf.py
# old bailey
#
# compute TF/IDF for each term used in a trial and
# sort in descending order

import os, sys, re
from math import log
from pysqlite2 import dbapi2 as sqlite

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

# given a list of words, remove any that are
# in a list of stop words
def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

# given a list of words, remove any that include numerals
def removeNumeralwords(wordlist):
    numerals = re.compile('\d+')
    l = wordlist[:]
    for m in l:
        if numerals.match(m):
            wordlist.remove(m)
    return wordlist

# given a directory string, return a list of file names
def getFileNames(dirstr):
    dircommand = 'dir ' + dirstr + ' /B'
    filelist = os.popen(dircommand).readlines()
    filelist = [x.rstrip() for x in filelist]
    return filelist

# trials
trialdir = 'Mined_1840s_clean'
triallist = getFileNames(trialdir)
numdocs = len(triallist)

# create tfidf directory if it doesn't exist
tfidfdir = 'TFIDF_1840s'
if os.path.exists(tfidfdir) == 0: os.mkdir(tfidfdir)

# look up document frequencies in SQLite DB
connection = sqlite.connect('docfreqs1840s.db')
cursor = connection.cursor()

# process each trial
i = 0
for t in triallist:
    
    # provide feedback for user
    i += 1
    print 'Processing %06d %s' % (i, t)
    sys.stdout.flush()
    
    # create a dictionary of unique words and word counts from trial
    trialstr = ''
    trialstr = open(trialdir + '\\' + t, 'r').read()
    allwords = trialstr.split(' ')
    wordlist = removeStopwords(allwords, stopwords)
    wordlist = removeNumeralwords(wordlist)
    wordfreq = [wordlist.count(p) for p in wordlist]
    dictionary = dict(zip(wordlist,wordfreq))
    
    # compute TF/IDF for each term and add to a new dictionary
    newdict = {}
    for key in dictionary:
        getdf = cursor.execute("SELECT freq FROM docfreqs1840s WHERE docterm = '%s'" % (key)).fetchone()
        if getdf == None:
            print "ERROR: No doc freq for %s" % key
            quit()
        df = float(getdf[0])
        tf = float(dictionary[key])
        tfidf = log(tf+1.0) * log(numdocs/df)
        newdict[key] = tfidf
    
    # sort TF/IDFs in descending order
    aux = [ (newdict[key], key) for key in newdict]
    aux.sort()
    aux.reverse()
        
    # write out to text file
    trialpattern = re.compile(r'clean_(t-\d+-\d+)', re.UNICODE)
    matchid = trialpattern.search(str(t))
    outfile = tfidfdir + '\\' + 'tfidf_' + matchid.group(1) + '.txt'
    f = open(outfile, 'w')
    for a in aux:
        f.write(str(a[1]) + ',' + str(a[0]) + '\n')
    f.close()
    