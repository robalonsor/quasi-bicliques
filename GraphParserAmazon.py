#!/usr/bin python3

# this code is intended to parse a portion of the Amazon dataset to a Graphml file
# Input: Amazon dataset
# Output: A graphphml representing a bipartite graph (e.g. user-reviews, user-purchases)

f = open("raw/short_out.amazon-ratings")
# f = open("raw/test.amazon")

edges = ""
nodes = ""
edge_set = set()
unique_id = 0
node_set_A = set()
node_set_B = set()
for line in f:
    data = line.split()
    edge_set.add((data[0], data[1]))
f.close()
max_num = -1

for edge in edge_set:
    if max_num < int(edge[0]):
        max_num = int(edge[0])
print("max num found: ", max_num)

for edge in edge_set:
    # we will use max_num to ensure unique values in vertices
    edges += '<edge source="'+edge[0]+'" target="'+str(int(edge[1])+max_num)+'" g1="100"/>\n'
    node_set_A.add(edge[0])
    node_set_B.add(edge[1])

for node in node_set_A:
    nodes += '<node id="'+node+'" type="A"/>\n'

for node in node_set_B:
    nodes += '<node id="' + str(int(node)+max_num) + '" type="B"/>\n'
##
## Writing Graphml file

output = '<?xml version="1.0" encoding="UTF-8"?>\n' \
         '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://' \
         'www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.' \
         'org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n<graph id="G" edged' \
         'efault="undirected">\n'
output += nodes+edges+'</graph>\n</graphml>'
import time
import calendar
newfile = open("amazon"+str(calendar.timegm(time.gmtime()))+".graphml","w")
newfile.write(output)
newfile.close()

