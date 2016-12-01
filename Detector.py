#!/usr/bin python3



# A = [0,1,2,3,4,5,6,7,8]
from GraphFileReader import GraphFileReader
from Vertex import Vertex
from Cluster import Cluster
import PruneTechniques
import time  # Only works in Linux


##
# Pruning based in the 'interestingness' of the QBC
# msu controls the min. number of vertices type u
# msv controls the min. number of vertices type v
msv = 2  # First pruning technique.
msu = 2  # First pruning technique.
##

# Relative size of the QBC
g_min = 0.5  # Gamma min
l_min = 0.5  # Lambda min

c = 0  # Number of expansions performed
check = 0  # Number of visits to Enumeration Tree (to check for clusters)

clusterList = []  # List containing the clusters found


def miqu(U, V, candU, candV, _type, g):
    global c
    global check
    c += 1
    print(_type, U, V, "Cand_sets = ", candU, candV, "-*-")

    # candU, candV = PruneTechniques.prune_vertices(U, V, candU, candV, g)

    if len(U) >= msu and len(V) >= msv:
        try:
            check += 1
            print("\tLooking for cluster in: ", U, V)
            vertices_by_type = g.split_vertices()  # a list with two positions [setA, setB]
            vertices_a = vertices_by_type[0]
            vertices_b = vertices_by_type[1]
            # print("\t", vertices_a, vertices_b)  # delete

            #  First check
            gamma_min_edges = round(len(U)*g_min, 0)  # min number of edges to be a QBC
            lambda_min_edges = round(len(V)*l_min, 0)  # min number of edges to be a QBC

            for u in U:
                u_edges = 0
                if Vertex(u, "a") not in vertices_a:
                    raise Exception("Vertex", u, " not in list of vertices")
                for v in V:
                    if Vertex(v, "b") not in vertices_b:
                        raise Exception("Vertex", v, " not in list of vertices")
                    u_in_g = {x for x in vertices_a if x == Vertex(u, "a")}.pop()
                    v_in_g = {x for x in vertices_b if x == Vertex(v, "b")}.pop()
                    e = u_in_g.get_edge_to(0, v_in_g)
                    # e = u_in_g.get_edge_to(0, Vertex(5, "b"))
                    if e is None:
                        # raise Exception("No such edge, between ", u_in_g, v_in_g)
                        continue
                    # print(e)
                    u_edges += 1
                    if u_edges >= gamma_min_edges:  # reached the ideal number of edges for the vertex u
                        break  # optimization, no need to check further if curr. belongs to a QBC

                if u_edges < gamma_min_edges:
                    raise Exception("One vertex from U (", u, ") w/o enough edges to form a QBC with", v)

                    # retrieve element
            # print("Num of u edges", u_edges)
            # at this point,
            # u and v are in in G or CC
            for v in V:
                v_edges = 0
                for u in U:
                    u_in_g = {x for x in vertices_a if x == Vertex(u, "a")}.pop()
                    v_in_g = {x for x in vertices_b if x == Vertex(v, "b")}.pop()
                    e = u_in_g.get_edge_to(0, v_in_g)
                    # e = u_in_g.get_edge_to(0, Vertex(5, "b"))
                    if e is None:
                        # raise Exception("No such edge, between ", u_in_g, v_in_g)
                        continue
                    # print(e)
                    v_edges += 1
                    if v_edges >= lambda_min_edges: # reached the ideal number of edges for vertex v
                        break
                if v_edges < lambda_min_edges:  # if the min # of edges v is less than v_edge, v cannot be part of a QBC
                    raise Exception("One vertex from V (", v, ") w/o enough edges to form a QBC with ", u)

            # if u_edges >= gamma_min_edges and v_edges >= lambda_min_edges:
            # at this point there is no way U, V are not a cluster
            print("\tCluster! ")
            # clusterList.append([U, V])
            clusterList.append(Cluster(U, V))
            # at this point we are sure that u,v are in the graph

        except Exception as er:
            print("\t", er, "!!!!")
        finally:
            pass

    if len(U) >= len(A) and len(V) >= len(B):
        # print("No more U or V expansion: Max. QB in G")
        return
    # U-expansion
    if len(V) >= msv:
        i = 0
        while i < len(candU):
            if U[-1] >= max(candU):  # or U[-1] >= candU[0]:
                break
            copyOfCandU = list(candU)
            copyOfCandU.pop(i)
            copyOfU = list(U)
            copyOfU.append(candU[i])
            i += 1
            if copyOfU[-1] < copyOfU[-2]:
                continue
            miqu(copyOfU, V, copyOfCandU, [], "U",g)
    # V-expansion
    if len(U) >= msu:
        i = 0
        while i < len(candV):
            if V[-1] >= max(candV):  # or V[-1] >= candV[0]:
                break
            copyOfCandV = list(candV)
            copyOfCandV.pop(i)
            copyOfV = list(V)
            copyOfV.append(candV[i])
            i += 1
            if copyOfV[-1] < copyOfV[-2]:
                continue
            miqu(U, copyOfV, [], copyOfCandV, "V",g)
    i = 0
    while i < len(candU):
        j = 0
        while j < len(candV):
            copyOfU = list(U)
            copyOfV = list(V)
            copyOfU.append(candU[i])
            copyOfV.append(candV[j])
            if len(U) > 0:
                if copyOfU[-1] < copyOfU[-2]:
                    # copyOfU = copyOfU[:-1]
                    j += 1
                    continue
            if len(V) > 0:
                if copyOfV[-1] < copyOfV[-2]:
                    # copyOfV = copyOfV[:-1]
                    j += 1
                    continue

            # copyOfCandU = list(candU)
            copyOfCandU = candU[:]
            copyOfCandU.pop(i)
            # copyOfCandV = list(candV)
            copyOfCandV = candV[:]
            copyOfCandV.pop(j)

            if len(U) > 0 and len(V) > 0:
                if V[-1] >= max(candV) or U[-1] >= max(candU):
                    print ("Not expanding:  ", U, V, candU, candV)
                    break
            # print "----> ", candU, candV
            miqu(copyOfU, copyOfV, copyOfCandU, copyOfCandV, "U-V",g)

            j += 1
        i -= 1
        candU.pop(0)
        i += 1

g_reader = GraphFileReader("datasets/bipartite.graphml")
g_reader.generate_graph()
g = g_reader.graph
# print(g)

AB = g.split_vertices()

A = AB[0]
B = AB[1]

A = list(str(A).replace('*','').replace('{','').replace(',','').replace('}','').replace(' ',''))
A = [int(x) for x in A]
B = list(str(B).replace('+','').replace('{','').replace(',','').replace('}','').replace(' ',''))
B = [int(x) for x in B]
B.sort()
A.sort()

print(A)
print(B)
#print("printing", list(str(A).replace('*','').replace('{','').replace(',','').replace('}','').replace(' ','')))
#exit()
# A = [0, 1]
# B = [2, 3, 4]
elapsed_time = time.clock()
miqu([], [], A, B, "U-V", g)
final_time = time.clock()-elapsed_time
print("*************\nNumber of visits to enum. tree", c)
print("Number of actual checks (for cluster)", check)
print("The following clusters have been found:  ")
print("Time:  ", final_time)  # Consider processing of QBC, i.e. loading time (from file to graph) not considered

# print(clusterList)
for c in clusterList:
    print(c)
# print([''.join(each) for each in clusterList])
