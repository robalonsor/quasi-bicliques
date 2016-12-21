#!/usr/bin python3

import configparser
import networkx as nx
# from GraphFileReader import GraphFileReader
# from Vertex import Vertex
# from Cluster import Cluster
# import matplotlib.pyplot as plt

def str_to_bool(v):
    return v.lower() == "true"

def prune_vertices(U, V, candU, candV, g, params, config_info):
    config = configparser.ConfigParser()
    config.read_dict(config_info)

    # Storing in a dict function calls
    dict_of_prun_tech = {'degree': prune_based_on_degree, 'diameter': prune_based_on_diameter}

    # if all flags are disabled
    # return the same vertices
    # return U, V
    fail_flag = False

    for prun_tech in config['PruneSection']:
        g_structure = g.subgraph(U + V + candU + candV) # creating networkx subgraph
        if config['PruneSection'][prun_tech].lower() == "true": # if prun tech 'prun_tech' is true, activate
            debug_output = str_to_bool(config['DebugOption']['prune_debug'])
            candU, candV, fail_flag = dict_of_prun_tech[prun_tech](U, V, candU, candV, g_structure, params, debug_output)

    # candU, candV, fail_flag = prune_based_on_diameter(U, V, candU, candV, g_structure)
    # g_structure = G.subgraph(U + V + candU + candV)
    # candU, candV, fail_flag = prune_based_on_degree(U, V, candU, candV, g_structure, params)

    if config['DebugOption']['prune_debug'].lower() == "true":
        print("****No more pruning for the node in enumeration tree****")
        print("After prun.tech., for ST, cand sets are", candU, candV)

    candU.sort()
    candV.sort()

    return candU, candV, fail_flag

def pre_processing(vertices_a, vertices_b, g):
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

def prune_based_on_degree(U, V, candU, candV, g_structure, params, debug_output):
    # params position 0=gamma position 1=lambda
    if debug_output:
        print("Starting pruning based on degree")
        print(U, V, candU, candV)

    # min_edges_u = round((len(V) + 1) * params[1],0)
    # min_edges_v = round((len(U) + 1) * params[0],0) # all v in V must have these edges
    min_edges_u = round((len(V)) * params[1], 0)
    min_edges_v = round((len(U)) * params[0], 0)  # all v in candV must have these edges
    if debug_output:
        print("min edges for u = ",min_edges_u, " and for v = ", min_edges_v)

    keep_pruning = True
    while keep_pruning:
        keep_pruning = False
        # g_structure = g_structure.subgraph(U + V + candU + candV)
        degree_vertex_u = g_structure.degree(candU)
        degree_vertex_v = g_structure.degree(candV)
        for u in candU:
            if g_structure.degree(u) < min_edges_u:
                g_structure.remove_node(u)
                # print("deleting....",candU.pop(candU.index(u)))
                candU.pop(candU.index(u))
                keep_pruning = True
                break
        for v in candV:
            if g_structure.degree(v) < min_edges_v:
                g_structure.remove_node(v)
                # print("deleting...", candV.pop(candV.index(v)))
                candV.pop(candV.index(v))
                keep_pruning = True
                break
    if debug_output:
        # print("deg->", nx.to_dict_of_lists(g_structure))
        print("Deg. candidates after prun: ",candU,candV)


    return candU,candV,False

# TODO: Correct this pruning techique since there is a bug that prunes candidates that are part of a QBC
def prune_based_on_diameter(U, V, candU, candV, g_structure, params, debug_output):
    if debug_output:
        print("Starting pruning based on diameter")
        print(U, V, candU, candV)
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
    if debug_output:
        print("After computing diameter the intersection of vertices is: ")
        print(intersection_of_vertices)
        print("Deleting candidates not in the intersection")
        print("Current candidates", candU, candV)
    candU = [item for item in candU if item in intersection_of_vertices]
    candV = [item for item in candV if item in intersection_of_vertices]

    if debug_output:
        print("Diam. After diam. prun. candidates are: ", candU, candV)

    return candU, candV, False

# g_reader = GraphFileReader("datasets/bipartite.graphml")
# g_reader.generate_graph()
# g = g_reader.graph
#
# g2 = nx.Graph(g.to_dict_of_lists(0))
# #
# # # diameter pruning test
# prune_vertices([7, 8], [6, 9], [1, 3, 5], [2, 4], g2, [0.5, 0.5])

# prune_vertices([], [], [], [], g)
#
# for n, d in G_structure.nodes_iter(data=True):
#     print(type(n))
#     print(n, nx.single_source_shortest_path_length(G_structure, n, 2))
#
# nx.draw(G_structure, pos=nx.spring_layout(G_structure), with_labels=True)
#
# plt.show()
