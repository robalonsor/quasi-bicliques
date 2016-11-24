#!/usr/bin python3

# Expansion tree as described in 2010-2011.
# Mining Cross Graph Quasi-Biclique for
# Financial Stock and Ratios

# A = [0,1,2,3,4,5,6,7,8]
from GraphFileReader import GraphFileReader
from Vertex import Vertex

msv = 1
msu = 1

g_min = 0.5  # Gamma min
l_min = 0.5  # Lambda min

c = 0
check = 0

clusterList = []

def miqu(U, V, candU, candV, _type, g):
    global c
    global check
    c += 1
    print(_type, U, V, "Cand_sets = ", candU, candV,"-*-")
    if len(U) >= msu and len(V) >= msv:
        try:
            check += 1
            print("\tLooking for cluser in: ", U, V)
            vertices_by_type = g.split_vertices()  # a list with two positions [setA, setB]
            vertices_a = vertices_by_type[0]
            vertices_b = vertices_by_type[1]
            print("\t", vertices_a, vertices_b)  # delete

            #  First check
            gamma_min_edges = round(len(U)*g_min,0)  # min number of edges
            lambda_min_edges = round(len(V)*l_min,0)  # min number of edges
            u_edges = 0
            v_edges = 0

            for u in U:
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
                        raise Exception("No such edge")
                    print(e)
                    u_edges += 1
                    if u_edges >= gamma_min_edges: # reached the ideal number of edges
                        break
                    # retrieve element
            print("Num of u edges", u_edges)
            # u and v are in in G
            for v in V:
                for u in U:
                    u_in_g = {x for x in vertices_a if x == Vertex(u, "a")}.pop()
                    v_in_g = {x for x in vertices_b if x == Vertex(v, "b")}.pop()
                    e = u_in_g.get_edge_to(0, v_in_g)
                    # e = u_in_g.get_edge_to(0, Vertex(5, "b"))
                    if e is None:
                        raise Exception("No such edge")
                    print(e)
                    v_edges += 1
                    if v_edges >= lambda_min_edges: # reached the ideal number of edges
                        break

            if u_edges >= gamma_min_edges and v_edges >= lambda_min_edges:
                print("Cluster!! ")
                clusterList.append([U,V])
            # at this point we are sure that u,v are in the graph

        except Exception as er:
            print(er, "!!!!")
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

miqu([], [], A, B, "U-V", g)
print("*************\nNumber of visits to enum. tree", c)
print("Number of actual checks (for cluster)", check)
print("The following clusters have been found:  ")
print(clusterList)