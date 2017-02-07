#!/usr/bin python3
# Brute-force approach
# to compute quasi-cliques (QC)
# given a graphml file
# since QC doesn't follow
# the antimonoticity property
# we need to check each possible
# combination


import PruneTechniques
import time  # Only works in Linux
import networkx as nx

from itertools import combinations

##
msu = 4
# Relative size of the QC
g_min = 0.5 # gamma min

c = 0  # Number of expansions performed
check = 0  # Number of visits to Enumeration Tree (to check for clusters)

clusterList = []  # List containing clusters found

def quasi_clique(U, g):
    global c
    global check
    c += 1
    O = [] # potential_quasi_clique

    # pre-processing
    # every vertex in CC must have at least msu*g_min edges, otherwise no quasi-clique

    u_min_edges = int(msu*g_min)

    print(len(U))
    for u in U.copy():
        if G.degree(u) < u_min_edges:
            U.remove(u)
    print(len(U))

    for combination in combinations(U,msu):
        H = g.subgraph(combination)
        if not nx.is_connected(H):
            continue
        print(combination)
        # break
    return
    if len(U) >= msu:
        # Pruning candidates when we have reached the minimum size constraint
        try:
            # check for connectedness of U+V. Since a QBC should be connected
            # G = nx.Graph(g.to_dict_of_lists(di))
            H = g.subgraph(U + V)
            if not nx.is_connected(H):
                raise Exception("Vertices U and V are not connected, so they cannot be part of an interesting QBC")
            candU, candV, fail_flag = PruneTechniques.prune_vertices(U, V, candU, candV, g, [g_min,l_min], config)
            if fail_flag:
                # something went wrong when pruning. e.g. a node is disconnected from G
                raise Exception("The current node in SET won't form a cluster")
            check += 1
            #  First check
            u_min_edges = round(len(V)*l_min, 0)  # all u in U must have these min number of edges to be a QBC
            for u in U:
                u_edges = 0
                for v in V:
                    if g.number_of_edges(u,v) >= 1:
                        u_edges += 1
                    if u_edges >= u_min_edges:  # reached the ideal number of edges for the vertex u
                        break  # optimization, no need to check further if curr. belongs to a QBC
                if u_edges < u_min_edges:
                    raise Exception("One vertex from U (", u, ") w/o enough edges to form a QBC with", v , " ---- edges",u_min_edges)

            print("\tCluster found! ")
            # clusterList.append([U, V])
            clusterList.append(Cluster(U, V))
            # at this point we are sure that u,v are in the graph
        except Exception as er:

            pass
        finally:
            pass


G = nx.read_graphml('datasets/bgb_two_att.graphml', node_type=int)

cc_list = list(nx.connected_component_subgraphs(G)) ## list of connected components

# Iterating through connected components
elapsed_time = time.clock() # Starting timer
for cc_index in range(len(cc_list)):
    cc = cc_list[cc_index]
    vertices_in_cc = set(cc.nodes())

    if len(vertices_in_cc) < msu:
        continue
    print("CC: ", vertices_in_cc)
    quasi_clique(vertices_in_cc, G)
    break

print("Total clusters found: ", len(clusterList))
print("The following clusters have been found:  ")
for c in clusterList:
    print(c)
