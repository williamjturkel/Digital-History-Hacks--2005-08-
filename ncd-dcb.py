# ncd-dcb.py
#
# Use Cilibrasi and Vitanyi's Normalized Compression Distance
# to cluster a randomly chosen sample of entries from the
# Dictionary of Canadian Biography volume 1
#
# wjt
# http://digitalhistoryhacks.blogspot.com
#
# 26 jun 2007

import bz2
import random

pathstring = 'C:\Documents and Settings\HP_Administrator\My Documents\digital-history-datasets\DCB-txt\DCB-v01-txt'

# Function to calculate the NCD of two files

def ncd(filex, filey):
    xbytes = open(filex, 'r').read()
    ybytes = open(filey, 'r').read()
    xybytes = xbytes + ybytes
    cx = bz2.compress(xbytes)
    cy = bz2.compress(ybytes)
    cxy = bz2.compress(xybytes)
    if len(cy) > len(cx):
        n = (len(cxy) - len(cx)) / float(len(cy))
    else:
        n = (len(cxy) - len(cy)) / float(len(cx))
    return n

# Randomly select 100 biographies from DCB vol 1 (nos. 34123-34714)

volume1 = range(34123, 34714)
selection = random.sample(volume1, 100)

# For each unique pair, calculate NCD

outfile = open('ncd-dcb.txt', 'w')
for i in range(0, len(selection)-1):
    print i
    for j in selection[i+1:]:
        fx = pathstring + '\\' + str(selection[i]) + '.txt'
        fy = pathstring + '\\' + str(j) + '.txt'
        outfile.write(str(selection[i]) + ", " + str(j) + ", " + str(ncd(fx, fy)) + "\n")

outfile.close()
    