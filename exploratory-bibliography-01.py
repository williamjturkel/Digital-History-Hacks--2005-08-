# exploratory-bibliography-01.py
#
# wjt
# 23-25 jan 2007
#
# http://digitalhistoryhacks.blogspot.com

import re, urllib, time
import xml.dom.minidom
from xml.dom.minidom import Node
import pickle

def scraper(url, filter=r'.*'):
    page = urllib.urlopen(url)
    pattern = re.compile(filter, re.IGNORECASE)
    returnlist = []
    for line in page.readlines():
        returnlist += pattern.findall(line)
    return returnlist

def get_similar(asin):
    baseurl = r'http://webservices.amazon.com/onca/xml?'
    service = r'Service=AWSECommerceService'
    amazonid = '1THTW69EYJTSND8GNA02'
    access = r'&AWSAccessKeyId=' + amazonid
    operation = r'&Operation=SimilarityLookup&ItemId=' + asin
    r = urllib.urlopen(baseurl + service + access + operation)
    return r

def get_text(nodelist):
    t = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            t = t + node.data
    return t

# scrape the bibliography to get a list of Amazon ASINs
biblio_url = r'http://digitalhistoryhacks.blogspot.com/2007/01/readings-for-field-in-digital-history.html'
book_pattern = '<a href="http://www.amazon.com/.*?(\d\d\d\d\d\d\d\d\d.).*?".*?>.*?</a>'
biblio_books = scraper(biblio_url, book_pattern)

# for each book in bibliography, get similar items
from_to = []
for b in biblio_books:
    results = ""
    doc = ""
    time.sleep(2)
    results = get_similar(b)
    doc = xml.dom.minidom.parse(results)
    print 'Processing ' + b + '\n'
    for sim in doc.getElementsByTagName("ASIN"):
        from_to.append((b, get_text(sim.childNodes)))
        
pickle.dump(from_to, open("tempstorage", "w"))
