# exploratory-bibliography-03.py
#
# wjt
# 27 jan 2007
#
# http://digitalhistoryhacks.blogspot.com

import pickle

from_to = pickle.load(open("tempstorage"))

# get the list of original books
original_books = list(set([ row[0] for row in from_to ]))

graph_file = open('expbib-03.txt', 'w')

graph_file.write('digraph G {\n')
graph_file.write('\tgraph [overlap=scale];\n')
graph_file.write('\tnode [color=steelblue3];\n')
for o in original_books:
    graph_file.write('\tA' + o + ' [color=lightblue2, style=filled];\n')
for o in range(0, len(original_books)):
    for p in range((o+1), len(original_books)):
        if ((original_books[o], original_books[p]) in from_to) & ((original_books[p], original_books[o]) in from_to):
            graph_file.write('\tA' + original_books[o] + ' -> A' + original_books[p] + ' [arrowhead=both];\n')
        elif (original_books[o], original_books[p]) in from_to:
            graph_file.write('\tA' + original_books[o] + ' -> A' + original_books[p] + ';\n')
        elif (original_books[p], original_books[o]) in from_to:
            graph_file.write('\tA' + original_books[p] + ' -> A' + original_books[o] + ';\n')
            
graph_file.write('}')

graph_file.close()