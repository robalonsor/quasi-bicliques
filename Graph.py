#!/usr/bin python3
from Edge import Edge
from Vertex import Vertex

# General Graph class for Bipartite and non-bipartite graphs

class Graph(object):
    def __init__(self, dimensionality):
        self.dimensionality = dimensionality  # an integer rep. num. of graphs, default: 2
        self.vertices = set()

    def __str__(self):
        s = "\n"
        list_edges = []
        for di in range(self.dimensionality):
            list_edges.append("edges dim: " + str(di))
            for v in self.vertices:
                # print(v.get_edges(di))
                for neighbor in v.get_edges(di):
                    if v == v.get_edges(di)[neighbor].vertex1:
                        list_edges.append(str(v.get_edges(di)[neighbor]))  # append the edge

        return s.join(list_edges)

    def __repr__(self):
        return self.__str__()

    # to_dict_of_lists is a function that receives # of dimension
    # returns: a dictionary of lists
    #          representing the graph in dimension <di>
    #          This can be used as the input of networkx
    def to_dict_of_lists(self, di):
        dol = {}
        for v in self.vertices:
            for neighbor in v.get_edges(di):
                if v != v.get_edges(di)[neighbor].vertex1:
                    continue
                e = v.get_edges(di)[neighbor]
                small_id = -1
                large_id = -1
                if e.vertex1.compare(e.vertex2) == 1:  # v1 id larger than v2
                    large_id = e.vertex1.vertex_id
                    small_id = e.vertex2.vertex_id
                else:
                    large_id = e.vertex2.vertex_id
                    small_id = e.vertex1.vertex_id
                assert small_id >= 0 and large_id >= 0

                if small_id in dol:
                    temp = dol[small_id]  # storing edges temporarily
                    temp.append(large_id)
                    dol[small_id] = temp
                else:
                    dol[small_id] = [large_id]
        return dol  # dict of list (#key->vertex id: value -> adj. list)

    def split_vertices(self):
        set_a = set()
        set_b = set()
        for v in self.vertices:
            if v.type_of_vertex == "a":
                set_a.add(v)
            else:
                set_b.add(v)
        return [set_a, set_b]

    def get_vertices(self):
        return self.vertices

    def get_vertex_by_id(self, id_vertex):
        for v in self.vertices:
            if v.vertex_id == id_vertex:
                return v
        return

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def add_edge(self, dimension, v1, v2, value):
        e = Edge(v1, v2, value)
        v1.add_edge(dimension, e)
        v2.add_edge(dimension, e)
        return e

    def get_edges(self, di):
        # Returns: A list with edges

        list_of_edges = []
        for v in self.vertices:
            for neighbor in v.get_neighbors(di):
                if v.vertex_id < neighbor.vertex_id:
                    e = v.get_edge_to(di,neighbor)
                    list_of_edges.append(e)

        return list_of_edges

    def get_number_of_edges(self, di):
        number_edges = 0
        for v in self.vertices:
            for neighbor in v.get_neighbors(di):
                if v.vertex_id < neighbor.vertex_id:
                    number_edges += 1

        return number_edges

    def set_vertices(self, vertices):
        self.vertices = vertices

# import matplotlib.pyplot as plt
# import networkx as nx
#
# g1 = Graph(2)
# v1 = Vertex(1, "A")
# v2 = Vertex(2, "B")
# e = Edge(v1, v2, 100)
#
# v1.add_edge(0,e)
# v2.add_edge(0,e)
# g1.add_vertex(v1)
# g1.add_vertex(v2)
#
# v1 = Vertex(3, "A")
# v2 = Vertex(4, "B")
# e = Edge(v1, v2, 200)
# v1.add_edge(0,e)
# v2.add_edge(0,e)
#
# g1.add_vertex(v1)
# g1.add_vertex(v2)
#
# v1 = Vertex(1, "A")
# # v2 = Vertex(4, "B")
# e = Edge(v1, v2, 50)
# v1.add_edge(0, e)
# v2.add_edge(0, e)
#
# g1.add_vertex(v1)
# g1.add_vertex(v2)
#
# print(g1.get_edges(0))
#
# x = g1.to_dict_of_lists(0)
# G=nx.Graph(x)
# plt.title('Graph | dimension: '+str(0))
# nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
#
# plt.show()

# g1 = Graph(2)
#
# v1 = Vertex(1, "A")
# v5 = Vertex(5, "A")
#
# v2 = Vertex(2, "B")
# v3 = Vertex(3, "B")
# v4 = Vertex(4, "B")
#
# e = Edge(v1, v2, 100)
# e2 = Edge(v1, v3, 100)
# e3 = Edge(v3, v5, 100)
# e4 = Edge(v5, v4, 100)
# e5 = Edge(v5,v2,100)
# e6 = Edge(v1,v4,100)
# v1.add_edge(0, e)
# v2.add_edge(0, e)
#
# v1.add_edge(0,e2)
# v3.add_edge(0,e2)
#
# # v3.add_edge(0,e3)
# # v5.add_edge(0,e3)
#
# v5.add_edge(0,e4)
# v4.add_edge(0,e4)
#
# v5.add_edge(0,e5)
# v2.add_edge(0,e5)
#
# v1.add_edge(0,e6)
# v4.add_edge(0,e6)
#
# g1.add_vertex(v1)
# g1.add_vertex(v2)
# g1.add_vertex(v3)
# g1.add_vertex(v4)
# g1.add_vertex(v5)
#
# e_dim2 = Edge(v3,v5,55)
# v3.add_edge(1,e_dim2)
# v5.add_edge(1,e_dim2)


#print(x)

#print(v1, v2)
#print(v1 != v2)

