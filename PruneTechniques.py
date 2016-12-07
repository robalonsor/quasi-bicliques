#!/usr/bin python3

from GraphFileReader import GraphFileReader
from Vertex import Vertex
from Cluster import Cluster
import networkx as nx
import matplotlib.pyplot as plt


def prune_vertices(U, V, candU, candV, g):

    # if all flags are disabled
    # flags for the pruning techniques
    # come from the Graphs class

    # return the same vertices
    # return U, V
    # vertices_by_type = g.split_vertices()  # a list with two positions [setA, setB]
    # vertices_a = vertices_by_type[0]
    # vertices_b = vertices_by_type[1]

    # vertices_a, vertices_b = prune_based_on_degree(vertices_a, vertices_b, g)

    g_structure = nx.Graph(g.to_dict_of_lists(0))  # graph from dimension 1

    candU, candV, fail_flag = prune_based_on_diameter(U, V, candU, candV, g_structure)

    print("\n\n****No more pruning for the node in enumeration tree****")
    print("At the end of pruning tech. cand sets are", candU, candV)

    candU.sort()
    candV.sort()

    #print(g.to_dict_of_lists(0))
    # print(U, V)

    return candU, candV, fail_flag

def prune_based_on_degree(vertices_a, vertices_b, g):
    keep_pruning = True  # We shall prune until no vertex is pruned
                         # This is because deleting a vertex from G
                         # may disconnect or reduce the degree of other
                         # vertices
    while keep_pruning:
        keep_pruning = False
        # print("Before deg. prun")
        # print(vertices_a, vertices_b)
        try:
            for u in vertices_a.copy():
                u_edges = 0
                for v in vertices_b:
                    e = u.get_edge_to(0, v)
                    if e is None:
                        # raise Exception("No such edge, between ", u_in_g, v_in_g)
                        continue
                    u_edges += 1
                if u_edges <= 1:
                    # raise Exception("Vertex  u = ", u, " with few edges. Deleting")
                    vertices_a.remove(u)
                    keep_pruning = True

            for v in vertices_b.copy():
                v_edges = 0
                for u in vertices_a:
                    e = u.get_edge_to(0, v)
                    if e is None:
                        # raise Exception("No such edge, between ", u_in_g, v_in_g)
                        continue
                    v_edges += 1
                if v_edges <= 1:  # if the min # of edges v is less than v_edge, v cannot be part of a QBC
                    # raise Exception("Vertex v = ", v, " with few edges. Deleting")
                    vertices_b.remove(v)
                    keep_pruning = True
        except Exception as er:
            print("\t", er, "!!!!")
        finally:
            pass
        # print("After deg. prun: ")
        # print(vertices_a, vertices_b)

    return vertices_a, vertices_b


def prune_based_on_diameter(U, V, candU, candV, g_structure):
    # print("Starting pruning based on diameter")
    # print(U, V, candU, candV)
    # g_structure = nx.Graph(g_structure.to_dict_of_lists(0))
    for u in U:
        if u not in g_structure:
            return candU, candV, True
    for v in V:
        if v not in g_structure:
            return candU, candV, True

    max_diameter = 4
    intersection_of_vertices = set()
    # for vertex, data in g_structure.nodes_iter(data=True):
    for vertex in U+V:
        neighbors_of_v = nx.single_source_shortest_path(g_structure, vertex, max_diameter)
        if intersection_of_vertices:
            # compute new intersection of vertices
            intersection_of_vertices = intersection_of_vertices.intersection(neighbors_of_v)
        else:
            intersection_of_vertices = set(neighbors_of_v.keys())
    # print("After computing diameter the intersection of vertices is: ")
    # print(intersection_of_vertices)
    # print("Deleting candidates not in the intersection")
    # print("Current candidates", candU, candV)
    candU = [item for item in candU if item in intersection_of_vertices]
    candV = [item for item in candV if item in intersection_of_vertices]
    print("After diam. prun. candidates are: ", candU, candV)

    return candU, candV, False

# g_reader = GraphFileReader("datasets/bipartite_toy1.graphml")
# g_reader.generate_graph()
# g = g_reader.graph
#
# # diameter pruning test
# prune_vertices([0, 1], [3, 6], [9], [5, 7], g)

# prune_vertices([], [], [], [], g)
#
# for n, d in G_structure.nodes_iter(data=True):
#     print(type(n))
#     print(n, nx.single_source_shortest_path_length(G_structure, n, 2))
#
# nx.draw(G_structure, pos=nx.spring_layout(G_structure), with_labels=True)
#
# plt.show()
