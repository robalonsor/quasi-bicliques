#!/usr/bin python3
from Graph import Graph
from Vertex import Vertex
from Edge import Edge

# import sys
import networkx as nx


class GraphFileReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.edge_set = {}
        self.vertex_type_dic = {}
        self.graph = Graph(2)

    def generate_graph(self):
        file_name = self.file_name
        try:
            f = open(file_name, 'r')
        except IOError:
            print('cannot open', file_name)
        else:
            print(file_name, 'has', len(f.readlines()), 'lines')
            print("Starting to parse Graphml file")
            f.close()
            self.construct_graph_from_file(file_name)

    # def get_graph(self):
    #     return self.graph

    def construct_graph_from_file(self, file_name):
        f = open(file_name)
        self.vertex_type_dic = {}
        try:
            for line in f:
                if "<edge source=" in line:
                    break
                if "<node id=" in line:
                    if "type" not in line:
                        raise Exception("Error! Found vertex without a type. Exit")
                    line = line[10:]
                    stop = line.index('"')
                    v_id = int(line[0:stop])
                    line = line[stop+8:]
                    stop = line.index('"')
                    v_type = line[0:stop]
                    if v_id in self.vertex_type_dic:
                        raise Exception("Error! Possible duplicate vertex. Exit")
                    self.vertex_type_dic[v_id] = v_type

            f.close()
            assert len(self.vertex_type_dic) > 1
        except Exception as er:
            print(er)
            return

        print("Successfully constructed vertex set")
        print(self.vertex_type_dic)
        print("Constructing edge set")

        G = nx.read_graphml(f.name, node_type=int)  # Constr. edge set using networkx+graphml reader
        print(nx.to_dict_of_lists(G))
        self.edge_set = nx.to_dict_of_lists(G)
        self.graph_construction()

    def graph_construction(self):
        V_type = self.vertex_type_dic  # vertex type
        E = self.edge_set  # set of edges
        g = self.graph
        for key_v_id in E:
            edges_to = E[key_v_id]  # the list of vertices with edge to <key_v_id> vertex
            v1 = Vertex(key_v_id, V_type[key_v_id])
            for v in edges_to:
                v2 = Vertex(v, V_type[v])
                e = Edge(v1, v2, 100)  # 100 is an arbitrary value
                v1.add_edge(0, e)
            g.add_vertex(v1)
        self.graph = g
        if g:
            return True
        return

        # v1 = Vertex(1, "A")
        # v2 = Vertex(2, "B")
        # e = Edge(v1, v2, 100)
        #
        # v1.add_edge(0,e)
        # v2.add_edge(0,e)
        # g1.add_vertex(v1)
        # g1.add_vertex(v2)




# g_reader = GraphFileReader("datasets/bipartite.graphml")
# g_reader.generate_graph()
# g = g_reader.graph
# #
# G = nx.Graph(g.to_dict_of_lists(0))
#
# import matplotlib.pyplot as plt
# nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
# plt.show()

