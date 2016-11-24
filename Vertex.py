#!/usr/bin python3

# Class Vertex
# for MiQuBic
# import Edge


class Vertex(object):
    def __init__(self, vertex_id, type_of_vertex):
        self.vertex_id = vertex_id
        self.type_of_vertex = type_of_vertex.lower()
        self.adjLists = [{}, {}]  # One adj list per graph/dimension
        # ArrayList < HashMap < Node, Edge >> adjLists = new  ArrayList < HashMap < Node, Edge >> ();

    def __str__(self):
        if self.type_of_vertex == "a":
            return str(self.vertex_id) + "*"  # Vertex type U
        return str(self.vertex_id)+"+"  # Vertex type V

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.vertex_id == other.vertex_id) and (self.type_of_vertex == other.type_of_vertex)

    def __hash__(self):
        return hash("x" * self.vertex_id)

    def initialize(self, graph_dimensionality):
        self.adjLists = [{}, {}]

    def same_type_as(self, other_vertex):
        if self.type_of_vertex == other_vertex.type_of_vertex:
            return True
        return False

    def compare(self, other_vertex):
        if self.vertex_id < other_vertex.vertex_id: return -1
        if self.vertex_id > other_vertex.vertex_id: return 1
        return 0

    def get_edges(self, di):
        return self.adjLists[di]  # returns a dictionary (key (node)->dim values: <Edges>

    def get_edge_to(self, di, neighbor):
        if neighbor not in self.adjLists[di]:
            return
        return self.adjLists[di][neighbor]

    def get_neighbors(self, di):
        return self.adjLists[di].keys()

    def add_edge(self, di, e):
        self.adjLists[di][e.get_other_vertex(self)] = e

    def delete_edge(self, di, e):
        self.adjLists[di].pop(e.get_other_vertex(self))

    def has_neighbor_in(self, di, vertices):
        adj_list = self.adjLists[di]
        for v in vertices:
            if adj_list[v]:
                return True
        return False

    def max_total_degree(self, di, restriction):
        degree = 0
        for neighbor in self.get_neighbors(di):
            if neighbor not in restriction:
                continue
            degree += 1
        return degree

# n = Vertex(1, "a")
# n.type_of_node = "b"
# print(n)
