# exploratory-bibliography-06.py
#
# wjt
# 2 feb 2007
#
# http://digitalhistoryhacks.blogspot.com

# chronological strata in recommendations
# (I know this is really ugly and inefficient)

import urllib, time
import xml.dom.minidom
from xml.dom.minidom import Node
import pickle
import anydbm

def get_text(nodelist):
    t = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            t = t + node.data
    return t

def get_pubyear(asin):
    pubdate = '0000-00-00'
    baseurl = r'http://webservices.amazon.com/onca/xml?'
    service = r'Service=AWSECommerceService'
    amazonid = '1THTW69EYJTSND8GNA02'
    access = r'&AWSAccessKeyId=' + amazonid
    operation = r'&Operation=ItemLookup&ItemId=' + asin
    response = r'&ResponseGroup=ItemAttributes'
    r = urllib.urlopen(baseurl + service + access + operation + response)
    doc = xml.dom.minidom.parse(r)
    for pd in doc.getElementsByTagName("PublicationDate"):
        pubdate = get_text(pd.childNodes)
    return pubdate[0:4]

def incrpair(ftdict, ftkey):
    if ftdict.has_key(ftkey):
        ftdict[ftkey] = str(int(ftdict[ftkey]) + 1)
    else:
        ftdict[ftkey] = "1"
    
from_to = pickle.load(open('tempstorage'))

to_go = len(from_to)

for ftpair in from_to:
    from_to_years = anydbm.open('from-to-years', 'c')
    checklist = anydbm.open('checklist', 'c')
    if str(ftpair) in checklist.keys():
        print str(to_go) + " Already did " + str(ftpair)
    else:
        print str(to_go) + " Processing " + str(ftpair)
        time.sleep(1.2)
        fyear = get_pubyear(ftpair[0])
        time.sleep(1.2)
        tyear = get_pubyear(ftpair[1])
        yearpair = str(fyear + " - " + tyear)
        print yearpair
        incrpair(from_to_years, yearpair)
        checklist[str(ftpair)] = "1"
    to_go = to_go - 1
    from_to_years.close()
    checklist.close()

from_to_years = anydbm.open('from-to-years', 'c')
outfile = open('from-to-years.csv', 'w')

for k in from_to_years.keys():
    outstr = k[0:4] + ',' + k[7:11] + ',' + from_to_years[k] + "\n"
    outfile.write(outstr)
    
from_to_years.close()
outfile.close()