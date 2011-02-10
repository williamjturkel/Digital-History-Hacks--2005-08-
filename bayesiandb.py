# bayesiandb.py
# old bailey
#
# naive bayesian learner
# adapted from Segaran, Programming Collective Intelligence, Ch. 6
# persists training info in SQLite DB

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
stopwords += ['yours', 'yourself', 'yourselves', '1', '2', '3', '4', '5']
stopwords += ['6', '7', '8', '9', '10']

# given a list of words, remove any that are
# in a list of stop words

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

# my version of this function removes stop words
# input is a string, output is a dictionary

def getwords(doc):
    allwords = doc.split(' ')
    wordlist = removeStopwords(allwords, stopwords)
    return dict([(w,1) for w in wordlist])

# alternative to getwords returns unique
# ngrams instead

def gettwograms(doc):
    allwords = doc.split(' ')
    wordlist = removeStopwords(allwords, stopwords)
    ngrams = [' '.join(wordlist[i:i+2]) for i in range(len(wordlist)-1)]
    return dict([(w,1) for w in ngrams])

def getthreegrams(doc):
    allwords = doc.split(' ')
    wordlist = removeStopwords(allwords, stopwords)
    ngrams = [' '.join(wordlist[i:i+3]) for i in range(len(wordlist)-2)]
    return dict([(w,1) for w in ngrams])

def getfourgrams(doc):
    allwords = doc.split(' ')
    wordlist = removeStopwords(allwords, stopwords)
    ngrams = [' '.join(wordlist[i:i+4]) for i in range(len(wordlist)-3)]
    return dict([(w,1) for w in ngrams])

# high tf/idf terms in n-gram context
def gettfidfngrams(doc):
    wordlist = doc.split('\n')
    return dict([(w,1) for w in wordlist])

# coinflip guessing function
def coinflip():
    import random
    r = random.randint(0, 1)
    if r: return 'y'
    else: return 'n'

class classifier:
    def __init__(self,getfeatures,filename=None):
        # count feature/category combinations
        self.fc={}
        # count documents in each category
        self.cc={}
        self.getfeatures=getfeatures
        # N.B. this isn't quite what Segaran has in the book
        self.thresholds={}
        
    def setthreshold(self,cat,t):
        self.thresholds[cat]=t
        
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]
    
    def setdb(self,dbfile):
        self.con=sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')
        
    # increase count of feature/category pair
    def incf(self,f,cat):
        count=self.fcount(f,cat)
        if count==0:
            self.con.execute("insert into fc values ('%s','%s',1)" % (f,cat))
        else:
            self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))
        
    # increase the count of a category
    def incc(self,cat):
        count=self.catcount(cat)
        if count==0:
            self.con.execute("insert into cc values ('%s',1)" % (cat))
        else:
            self.con.execute("update cc set count=%d where category='%s'" % (count+1,cat))
        
    # number of times a feature has appeared in a category
    def fcount(self,f,cat):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"' % (f,cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])
    
    # number of items in a category
    def catcount(self,cat):
        res=self.con.execute('select count from cc where category="%s"' % (cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    # total number of items
    def totalcount(self):
        res=self.con.execute('select sum(count) from cc').fetchone();
        if res==None: return 0
        else: return res[0]
    
    # list of all categories
    def categories(self):
        cur=self.con.execute('select category from cc');
        return [d[0] for d in cur]
    
    # take item (i.e., document) and classification
    def train(self,item,cat):
        features=self.getfeatures(item)
        # increment count for every feature with this category
        for f in features:
            self.incf(f,cat)
        # increment count for this category
        self.incc(cat)
        self.con.commit()
        
    # calculate probabilities
    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0
        # total number of times this feature appeared in this category
        # divided by total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    # calculate weighted probabilities
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # current probability
        basicprob=prf(f,cat)
        # number of times feature appeared in all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])
        # weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp
    
    def classify(self,item,default=None):
        probs={}
        # N.B. I added this
        best='n'
        # find category with highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat
        # make sure probability exceeds threshold times next best
        for cat in probs:
            if cat==best: continue
            # N.B. I modified this next line - complete kluge!
            if probs[cat]*self.getthreshold(best)>probs.get(best, 0.0): return default
            # if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best

class naivebayes(classifier):
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        # multiply probabilities of all features together
        p=1
        for f in features:
            p*=self.weightedprob(f,cat,self.fprob)
        return p
    
    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

########## test scaffolding begins

# def sampletrain(cl):
#    cl.train('the quick brown fox jumps','good')
#    cl.train('nobody owns the water','good')
#    cl.train('buy pharmaceuticals now','bad')
#    cl.train('make quick money at the online casino','bad')
#    cl.train('the quick rabbit jumps fences','good')
    
# cl=classifier(pcigetwords)
# sampletrain(cl)
# print "quick good"
# print cl.fcount('quick', 'good')
# print cl.fprob('quick', 'good')
# print "quick bad"
# print cl.fcount('quick', 'bad')
# print cl.fprob('quick', 'bad')
# print "casino good"
# print cl.fcount('casino', 'good')
# print cl.fprob('casino', 'good')
# print "casino bad"
# print cl.fcount('casino', 'bad')
# print cl.fprob('casino', 'bad')

# print "weightedprob first pass money good"
# print cl.weightedprob('money','good',cl.fprob)
# sampletrain(cl)
# print "weightedprob 2nd pass money good"
# print cl.weightedprob('money','good',cl.fprob)

# clnb=naivebayes(pcigetwords)
# sampletrain(clnb)
# print "quick rabbit good"
# print clnb.prob('quick rabbit','good')
# print "quick rabbit bad"
# print clnb.prob('quick rabbit','bad')
# print "quick rabbit classify"
# print clnb.classify('quick rabbit',default='unknown')
# print "quick money classify"
# print clnb.classify('quick money',default='unknown')

########## test scaffolding ends    
