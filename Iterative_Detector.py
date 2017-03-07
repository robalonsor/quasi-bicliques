#!/usr/bin python3
import networkx as nx
from operator import itemgetter
import time  # Only works in Linux
import itertools

__author__ = 'Roberto Alonso <robalonsor@gmail.com>'

# U = blue
# V = red

# Relative size of the QC
u_min = 1  # minimum size of the quasi-biclique
v_min = 1  # minimum size of the quasi-biclique

gamma_min = 0.5 # minimum density of the quasi-biclique
lambda_min = 0.5  # minimum density of the quasi-biclique

cluster_list = set()
debug_traversal = False

def node_to_tuple(O):
    return tuple(O[0]), tuple(O[1])

def detect_quasi_biclique(graph, cc):
    # Sorting according to degree. Considering this order, we expand the enumeration tree
    #TODO: fix sorting. should be sorted w.r.t tpye of vertex
    # sorted_vertices = sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)
    candidates_U_root = set(n for n, d in cc.nodes(data=True) if d['color'] == "red")
    candidates_V_root = set(graph) - candidates_U_root

    visited = set()

    k = min(u_min, v_min)
    # TODO: check if it make sense to make U-V expansion with u_min != v_min
    counter = 0 # the number of expansion conducted even if redundant
    actual_check = 0 # the real number of checked nodes
    while k <= len(candidates_U_root) and k <= len(candidates_V_root):
        for c in itertools.combinations(candidates_U_root, k):
            if k < u_min:
                continue
            for c_2 in itertools.combinations(candidates_V_root, k):
                if k < v_min:
                    continue
                #TODO: Make correctio in the expasion step. We need to consider combinations for curr node
                print("*Current main node:  ", c, c_2) if debug_traversal else False
                counter += 1
                actual_check += 1
                # Initializing candidate sets
                candidates_U = list(set(candidates_U_root) - set(c))
                candidates_V = list(set(candidates_V_root) - set(c_2))

                candidates_U.sort()
                candidates_V.sort()

                vertex_u_in_O = sorted(c)
                vertex_v_in_O = sorted(c_2)

                # the following stack is used in the U-expansion
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                # TODO: make corrections in the way we enumerate the tree
                visited.add(node_to_tuple(O))
                # U-expansion
                while len(candidates_U) > 0:
                    # O = stack_U[-1][0] #, stack_U[-1][1]]  # set O = {U,V}; potential quasi-biclique
                    counter += 1
                    print("\t(U-exp) O --> ", O, " candidates U->", candidates_U, " candidates V->", candidates_V) if debug_traversal else False
                    #print("Checking O", O)
                    # Expanding to the next vertex
                    # TODO: select better vertices considering e.g. degree
                    O[0].append(candidates_U.pop(0))
                    O[0].sort()
                    if node_to_tuple(O) in visited:
                        continue

                    visited.add(node_to_tuple(O))
                    actual_check += 1

                    if len(candidates_U) <= 0:
                        # check for QBC
                        print("\tFinally, checking ", O) if debug_traversal else False
                        actual_check += 1
                        #break
                # V-expansion
                #print(vertex_u_in_O)
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                # print("Starting V-expansion with:")
                # print(O, candidates_U, candidates_V)
                while len(candidates_V) > 0:
                    counter += 1
                    print("\t(V-exp) O --> ", O, " candidates U->", candidates_U, " candidates V->", candidates_V) if debug_traversal else False
                    #print("Checking O", O)
                    # Expanding to the next vertex
                    # TODO: select better vertices considering e.g. degree
                    O[1].append(candidates_V.pop(0))
                    O[1].sort()

                    if node_to_tuple(O) in visited:
                        continue
                    visited.add(node_to_tuple(O))
                    actual_check += 1
                    if len(candidates_V) <= 0:
                        # check for QBC
                        print("Finally, checking ", O) if debug_traversal else False
                        actual_check += 1
                        #break
                #exit()

        k += 1
        # break
    print(counter, actual_check)
    # exit()

def get_quasi_bicliques():
    # graph = nx.read_graphml('datasets/toy_bipartite.graphml', node_type=int)
    graph = nx.read_graphml('datasets/amazon.graphml', node_type=int)
    print("Looking for quasi bicliques with gamma <%s> density; lambda <%s> density "
          "and min. size of U = <%s> and V = <%s>"% (gamma_min, lambda_min, u_min, v_min))
    if not nx.is_bipartite(graph):
        print("Not a bipartite graph")
        return
    elapsed_time = time.time()  # Starting timer
    # TODO: pre-processing graph

    # color = nx.get_node_attributes(graph, 'color')
    # print("Att: ")
    # print(color)
    #
    cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
    # Iterating through connected components

    for cc in cc_list:
        if not nx.is_bipartite(cc):
            continue
        u_vertices = set(n for n, d in cc.nodes(data=True) if d['color'] == "red")
        v_vertices = set(graph) - u_vertices

        if len(v_vertices) < v_min or len(u_vertices) < u_min:
            continue
        print("CC of # vertices: |U| = %s ,  |V| = %s" % (len(u_vertices), len(v_vertices)))
        # global_tree_traverse = detect_quasi_biclique(graph, nx.subgraph(graph, vertices_in_cc))
        detect_quasi_biclique(graph, cc)
        print("End of CC")
        # break # TODO: delete after testing

    print("Quasi-bicliques in the graph: ", cluster_list)
    print("Total QBC in graph: ", len(cluster_list))
    final_time = time.time()-elapsed_time
    # print("# visits to SET: %s" % global_tree_traverse)

    print("runtime: %s" % final_time)

get_quasi_bicliques()