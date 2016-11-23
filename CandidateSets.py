#!/usr/bin python3
from Vertex import Vertex
from Edge import Edge


class CandidateSet(object):

    def __init__(self, dimension, connected_components, root=False, type_of_nodes=None):
        self.n_dimension = dimension  # Candidate set beloing to dimension n_dimension
        self.cc = connected_components  # connected components
        self.vertices_in_cand = set()
        self.vertices_type_a = set()
        self.vertices_type_b = set()
        self.type_of_nodes = type_of_nodes

        if root:
            self.create_root_node()
            return
        # connected_components contains candidate sets, and we create a copy
        self.create_child_node()

    def create_root_node(self):
        # WARNING! We are assuming that CC is a dict of lists in
        # networkx format eg {1:[1,2,3,4], 2:[1,0,3], 3:[1,2]...}
        # in networkx format, edges are repeated twice

        # not an optimal way, but faster to develop
        dic_v_type = self.type_of_nodes

        for key_v_id in self.cc:
            edges_to = dic_v_type[key_v_id]  # the list of vertices with edge to <key_v_id> vertex
            v1 = Vertex(key_v_id, dic_v_type[key_v_id])  # Creating vertex object
            for v in edges_to:
                v2 = Vertex(v, dic_v_type[v])
                e = Edge(v1, v2, 100)  # 100 is an arbitrary value
                v1.add_edge(0, e)
            if v1.type_of_vertex == "a":
                self.vertices_type_a.add(v1)
            else:
                self.vertices_type_b.add(v1)
            self.vertices_in_cand.add(v1)

        return True

    def create_child_node(self):
        # cc contains a set with all nodes

        if not isinstance(self.cc, set):
            print("Error while creating child node of enum. tree")
            print("CC does is not a set")
            return

        self.vertices_in_cand = self.cc
        # spliting vertices according to type
        for v in self.vertices_in_cand:
            if v.vertex_type == "a":
                self.vertices_type_a.add(v)
            else:
                self.vertices_type_b.add(v)

        return True
