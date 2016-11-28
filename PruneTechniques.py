#!/usr/bin python3

from GraphFileReader import GraphFileReader
from Vertex import Vertex
from Cluster import Cluster


def prune_vertices(U, V, g):

    # if all flagas are disabled
    # returnt he same vertices
    vertices_by_type = g.split_vertices()  # a list with two positions [setA, setB]
    vertices_a = vertices_by_type[0]
    vertices_b = vertices_by_type[1]

    U, V = prune_based_in_degree(vertices_a, vertices_b, g)
    return U, V


def prune_based_in_degree(vertices_a, vertices_b, g):
    print("Before deg. prun")
    print(vertices_a, vertices_b)
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
    except Exception as er:
        print("\t", er, "!!!!")
    finally:
        pass
    print("After deg. prun: ")
    print(vertices_a, vertices_b)

    return vertices_a, vertices_b


g_reader = GraphFileReader("datasets/bipartite.graphml")
g_reader.generate_graph()
g = g_reader.graph

prune_vertices([], [], g)
