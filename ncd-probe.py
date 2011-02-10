# ncd-probe.py
#
# Test with Radisson (DCB '35174')
#
# wjt
# http://digitalhistoryhacks.blogspot.com
#
# 1 jul 2007

from yahoo.search.web import WebSearch
import bz2
import random

# Frobisher
# pathstring = 'C:\Documents and Settings\HP_Administrator\My Documents\digital-history-datasets\DCB-txt\DCB-v01-txt'
# filex = pathstring + '\\' + '34352' + '.txt'

filex = '35174.txt'
xbytes = open(filex, 'r').read()
cx = bz2.compress(xbytes)

def ncd_probe(xbytes, cx, ybytes):
    # ybytes = open(filey, 'r').read()
    xybytes = xbytes + ybytes
    cy = bz2.compress(ybytes)
    cxy = bz2.compress(xybytes)
    n = (len(cxy) - len(cy)) / float(len(cx))
    return n

def printSortedDict(adict):
    keys = adict.keys()
    keys.sort()
    for k in keys:
        print k
        print adict[k]['Title']
        print adict[k]['Url']
        print adict[k]['Summary']
        print " "

app_id = "NCD-Probe-Demo"
srch = WebSearch(app_id, language='en')
srch.query = "Radisson"
srch.results = 50

dom = srch.get_results()
results = srch.parse_results(dom)

ranked = {}
for res in results:
    # strip out search word from summary
    summary = str(res['Summary'])
    stripped_summary = summary.replace('Radisson', '')
    distance = ncd_probe(xbytes, cx, stripped_summary)
    dstr = 'NCD: ' + str(distance)
    ranked[dstr] = res
 
printSortedDict(ranked)
