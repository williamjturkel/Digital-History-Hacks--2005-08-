# ncd-dcb-graph.py
#
# Use GraphViz to plot a network diagram of
# NCDs below some threshold
# using randomly chosen sample of entries from the
# Dictionary of Canadian Biography volume 1
#
# wjt
# http://digitalhistoryhacks.blogspot.com
#
# 26 jun 2007

threshold = 0.77

infile = open('ncd-dcb.txt', 'r')
rows = infile.readlines()
infile.close()

bios = []
links = []

for r in rows:
    row = r.split()
    if float(row[2]) < threshold:
        bios.append(row[0])
        bios.append(row[1])
        links.append(row)
        # print r,
        
print list(set(bios))
print links

graph_file = open('ncd-dcb-graph.txt', 'w')
graph_file.write('digraph G {\n')
graph_file.write('\tgraph [overlap=scale];\n')
graph_file.write('\tnode [color=steelblue3];\n')

bios = list(set(bios))
for b in bios:
    graph_file.write('\t' + b + ' [color=lightblue2, style=filled];\n')

for l in links:
    graph_file.write('\t' + l[0] + ' -> ' + l[1] + ' [arrowhead=both];\n')

graph_file.write('}')
graph_file.close()

#for o in original_books:
#    graph_file.write('\tA' + o + ' [color=lightblue2, style=filled];\n')
#for o in range(0, len(original_books)):
#    for p in range((o+1), len(original_books)):
#        if ((original_books[o], original_books[p]) in from_to) & ((original_books[p], original_books[o]) in from_to):
#            graph_file.write('\tA' + original_books[o] + ' -> A' + original_books[p] + ' [arrowhead=both];\n')
#        elif (original_books[o], original_books[p]) in from_to:
#            graph_file.write('\tA' + original_books[o] + ' -> A' + original_books[p] + ';\n')
#        elif (original_books[p], original_books[o]) in from_to:
#            graph_file.write('\tA' + original_books[p] + ' -> A' + original_books[o] + ';\n')
            
