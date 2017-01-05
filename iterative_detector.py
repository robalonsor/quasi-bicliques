#!/usr/bin python3
# WARNING! Looking for QBC size 2 weight 2
# will produce an error


# A = [0,1,2,3,4,5,6,7,8]
from GraphFileReader import GraphFileReader
from Cluster import Cluster
import PruneTechniques
import time  # Only works in Linux
import networkx as nx
import configparser
from itertools import combinations,chain

##
# Reading properties

config = configparser.ConfigParser()
config.read('ConfigFile.properties')
#
def powerset(iterable):
    "powerset recipe"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def str_to_bool(v):
    return v.lower() == "true"
##
# Pruning tech. based on the 'interestingness' of the QBC
# msu controls the min. number of vertices type u
# msv controls the min. number of vertices type v

msu = int(config['SizeSection']['msu'])  # First pruning technique.
msv = int(config['SizeSection']['msv'])  # First pruning technique.
##

# Relative size of the QBC
g_min = float(config['SizeSection']['gamma_min'])  # Gamma min
l_min = float(config['SizeSection']['lambda_min'])  # Lambda min

c = 0  # Number of expansions performed
check = 0  # Number of visits to Enumeration Tree (to check for clusters)

clusterList = []  # List containing clusters found
print("Consider that raise error execption log is disabled")

def miqu(U, V, candU, candV, _type, g, type_of_vertices, di = 0, ):
    global c
    global check
    c += 1
    if config['DebugOption']['expansion'].lower() == "true":
        print(_type, U, V, "Cand_sets = ", candU, candV, "-*-")

    try:
        val = powerset(candU)
        while True:
            x = val.__next__()
            print(x)
    except StopIteration:
        print("Iteration done.")

    # for U in powerset(candU):
    #     for V in powerset(candV):
    #         print(U,V)

    exit()

    if len(U) >= msu and len(V) >= msv:
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
            v_min_edges = round(len(U)*g_min, 0)  # likewise v in V min number of edges to be a QBC

            for u in U:
                u_edges = 0
                for v in V:
                    if g.number_of_edges(u,v) >= 1:
                        u_edges += 1
                    if u_edges >= u_min_edges:  # reached the ideal number of edges for the vertex u
                        break  # optimization, no need to check further if curr. belongs to a QBC
                if u_edges < u_min_edges:
                    raise Exception("One vertex from U (", u, ") w/o enough edges to form a QBC with", v , " ---- edges",u_min_edges)
            # at this point,
            # u and v are in in G or CC
            for v in V:
                v_edges = 0
                for u in U:
                    if g.number_of_edges(u,v) >=1:
                        v_edges += 1
                    if v_edges >= v_min_edges: # reached the ideal number of edges for vertex v
                        break
                if v_edges < v_min_edges:  # if the min # of edges v is less than v_edge, v cannot be part of a QBC
                    raise Exception("One vertex from V (", v, ") w/o enough edges to form a QBC with ", u)

            # if u_edges >= gamma_min_edges and v_edges >= lambda_min_edges:
            # at this point there is no way U, V are not a cluster
            if config['DebugOption']['cluster'].lower() == "true":
                print("\tCluster found! ")
            # clusterList.append([U, V])
            clusterList.append(Cluster(U, V))
            # at this point we are sure that u,v are in the graph
        except Exception as er:
            if config['DebugOption']['exception'].lower() == "true":
                print("\t Exp: ", er, "!!!!")
            pass
        finally:
            pass

    if len(U) >= len(A) and len(V) >= len(B):
        print("No more U or V expansion: Max. QB in G")
        return

g_reader = GraphFileReader(config['DataSetSection']['dataset'])
G = nx.read_graphml(config['DataSetSection']['dataset'],node_type=int)
g_reader.generate_graph()

cc_list = list(nx.connected_component_subgraphs(G)) ## list of connected components
# Splitting vertices according to type
A=set()
B=set()

for v_id in g_reader.vertex_type_dic:
    if g_reader.vertex_type_dic[v_id].lower() == "a":
        A.add(v_id)
    else:
        B.add(v_id)

# at this point A, B are sets of vertices U, V, respectively
# Iterating through connected components
elapsed_time = time.clock() # Starting timer
for cc_index in range(len(cc_list)):
    cc = cc_list[cc_index]

    # cc = cc_list[0]
    vertices_in_cc = set(cc.nodes())
    print("CC: ", vertices_in_cc)

    A_cc = A.intersection(vertices_in_cc)
    B_cc = B.intersection(vertices_in_cc)

    A_cc = list(A_cc)
    B_cc = list(B_cc)

    A_cc.sort()
    B_cc.sort()

    print(A_cc)
    print(B_cc)
    miqu([], [], A_cc, B_cc, "U-V", G, g_reader.vertex_type_dic)


total_a = len(A) # total num vertices type U in all graph
total_b = len(B) # total num vertices type V in all graph


final_time = time.clock()-elapsed_time
total_combinations = (2**total_a-1)*(2**total_b-1)
print("************\nTheoretical number of combinations to be explored", total_combinations)
print("*************\nNumber of visits to enum. tree", c)
print("Number of actual checks (for cluster)", check)
print("Minimum size of U and V, respectively", msu,msv)

print("Time:  ", final_time)  # Consider processing of QBC, i.e. loading time (from file to graph) not considered


print("Rules activated:")
rules = "*"
active_rules= []
if str_to_bool(config['PruneSection']['diameter']): active_rules.append("Diameter")
if str_to_bool(config['PruneSection']['degree']): active_rules.append("Degree")
active_rules = "*\n".join(active_rules)
print(active_rules)

#print("Minimum size of the QBC for U and V\nDiamaeter pruning of cand sets")
# print(clusterList)
print("Total clusters found: ", len(clusterList))
if str_to_bool(config['OutputFormat']['print_clusters']):
    print("The following clusters have been found:  ")
    for c in clusterList:
        print(c)
