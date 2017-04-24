#!/usr/bin python3
import networkx as nx
from operator import itemgetter
import time  # Only works in Linux
import itertools

__author__ = 'Roberto Alonso <robalonsor@gmail.com>'

# U = red
# V = blue

# Relative size of the QC
u_min = 1  # minimum size of the quasi-biclique
v_min = 1  # minimum size of the quasi-biclique

gamma_min = 0.5  # minimum density of the quasi-biclique
lambda_min = 0.5  # minimum density of the quasi-biclique

cluster_list = set()
debug_traversal = True
debug_traversal_u_set = True
debug_traversal_v_set = True
debug_traversal_visited = False
elapsed_time = time.time()

def detect_quasi_biclique(graph, cc):
    # Sorting according to degree. Considering this order, we expand the enumeration tree
    # TODO: fix sorting. should be sorted w.r.t type of vertex
    global debug_traversal
    global debug_traversal_u_set
    global debug_traversal_v_set
    global debug_traversal_visited
    # sorted_vertices = sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)
    candidates_U_root = set(n for n, d in cc.nodes(data=True) if d['color'] == "red")
    candidates_V_root = set(n for n, d in cc.nodes(data=True) if d['color'] == "blue")

    print(len(candidates_U_root))
    print(len(candidates_V_root))
    k = min(u_min, v_min)
    print(k)
    counter = 0 # the number of expansion conducted even if redundant
    actual_check = 0 # the real number of checked nodes
    visited = set()
    while k <= len(candidates_U_root) and k <= len(candidates_V_root):
        for c in itertools.combinations(candidates_U_root, k):
            # if k < u_min:
            #     continue
            for c_2 in itertools.combinations(candidates_V_root, k):

                # if k < v_min:
                #     continue

                print("*U-V expansion O -->  ", c, c_2) if debug_traversal else False
                counter += 1
                # actual_check += 1
                # Initializing candidate sets
                candidates_U = list(set(candidates_U_root) - set(c))
                candidates_V = list(set(candidates_V_root) - set(c_2))

                candidates_U.sort()
                candidates_V.sort()

                vertex_u_in_O = sorted(c)
                vertex_v_in_O = sorted(c_2)

                # the following stack is used in the U-expansion
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                # U-expansion
                U_stack = [[O[0], candidates_U]]  # initialization of stack for node
                # visited = set()
                while U_stack:
                    O_u = list(U_stack[-1][0])  # set O; potential quasi-clique
                    O_u.sort()
                    candidates = list(U_stack[-1][1])  # candidates to be part of the potential quasi-clique O
                    if (tuple(O_u), tuple(O[1])) not in visited and len(O_u) >= u_min:
                        # We have not visited current node
                        # so, we check for cluster
                        # Checking cluster
                        print("\t**(U-exp) O --> ", O_u, O[1], " candidates ->", candidates, []) if debug_traversal_u_set else False
                        actual_check += 1
                        visited.add((tuple(O_u), tuple(O[1])))

                        # TODO: Here we have to check if U, V is a QBC

                    # At this point we have checked for cluster
                    # if there are candidates, we expand

                    if len(candidates) == 0:
                        # print("\t  **(U-exp) Finally checking O set", O_u) if debug_traversal_u_set else False
                        U_stack.pop()
                        # actual_check += 1
                        continue
                    # TODO: select better vertices considering e.g. degree

                    # Expanding to the next suitable vertex

                    next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
                    U_stack[-1][1].pop(0)  # deleting from curr. node in enum. tree
                    print("\t  O+u_next=", tuple(O_u + [next_neighbor])) if debug_traversal_visited else False
                    print("\t  visited=", visited) if debug_traversal_visited else False

                    while (tuple(O_u + [next_neighbor]), tuple(O[1])) in visited and len(candidates) > 0:
                        next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
                    # TODO: Apparently, there are no edge cases that activate this rule (delete?)
                    # if tuple(O_u + [next_neighbor]) in visited:
                    #     # this means len(candidates) <= 0, so add this last element to stack
                    #     print("last element")
                    #     U_stack.pop()
                    #     visited.add(tuple(O_u))
                    #     continue
                    # At this point, we know that there is at least one
                    # vertex to use in the expansion step. We expand

                    O_u.append(next_neighbor)
                    O_u.sort()
                    U_stack.append([O_u, candidates])
                    # visited.add(tuple(O_u))
                    # visited.add((tuple(O_u), tuple(O[1])))
                    # print(visited)
                    # print("*", (tuple(O_u), tuple(O[1])))

                #
                # V-expansion
                #
                #
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                V_stack = [[O[1], candidates_V]]  # initialization of stack for node
                # visited = set()
                while V_stack:
                    O_v = list(V_stack[-1][0])  # set O; potential quasi-clique
                    O_v.sort()
                    if time.time()-elapsed_time > 100:
                        print("Killing... taking more than 300 seconds")
                        return
                    candidates = list(V_stack[-1][1])  # candidates to be part of the potential quasi-clique O
                    if (tuple(O[0]), tuple(O_v)) not in visited and len(O_v) >= v_min:
                        print("\t++(V-exp) O --> ", O[0], O_v, " candidates ->", [], candidates) if debug_traversal_v_set else False
                        visited.add((tuple(O[0]), tuple(O_v)))
                        actual_check += 1

                    if len(candidates) == 0:
                        # print("\t  ++(V-exp) Finally checking O set") if debug_traversal_v_set else False
                        V_stack.pop()
                        # actual_check += 1
                        continue
                    # TODO: select better vertices considering e.g. degree
                    # Expanding to the next suitable vertex
                    next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
                    V_stack[-1][1].pop(0)  # deleting from curr. node in enum. tree

                    print("\t  O+v_next=", tuple(O_v + [next_neighbor])) if debug_traversal_visited else False
                    print("\t  visited=", visited) if debug_traversal_visited else False

                    while (tuple(O[0]), tuple(O_v + [next_neighbor])) in visited and len(candidates) > 0:
                        next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
                    # actual_check += 1
                    O_v.append(next_neighbor)
                    O_v.sort()
                    V_stack.append([O_v, candidates])
                    # visited.add(tuple(O_v))
                    # visited.add((tuple(O[0]), tuple(O_v)))
                    # if len(O_v) > 50:
                    #     exit()

        k += 1
        # break
    # print(visited)
    print(counter, actual_check)
    # exit()


def get_quasi_bicliques():
    # graph = nx.read_graphml('datasets/toy_bipartite.graphml', node_type=int)
    graph = nx.read_graphml('datasets/bipartite.graphml', node_type=int)
    print("Looking for quasi bicliques with gamma <%s> density; lambda <%s> density "
          "and min. size of U = <%s> and V = <%s>"% (gamma_min, lambda_min, u_min, v_min))
    if not nx.is_bipartite(graph):
        print("Not a bipartite graph")
        return
    elapsed_time = time.time()  # Starting timer
    # TODO: pre-processing graph
    #
    cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
    # Iterating through connected components

    for cc in cc_list:
        if not nx.is_bipartite(cc):
            continue
        u_vertices = set(n for n, d in cc.nodes(data=True) if d['color'] == "red")
        v_vertices = set(n for n, d in cc.nodes(data=True) if d['color'] == "blue")

        # v_vertices = set(graph) - u_vertices  # TODO: re-enable this after pre-processing completed
                                                # the current problem is that if there are disconnected \
                                                # red nodes, u_vertices contains them, and v_vertices fails

        if len(v_vertices) < v_min or len(u_vertices) < u_min:
            print("skipping CC", v_min,u_min)
            continue
        print("CC of # vertices: |U| = %s ,  |V| = %s   tota nodes SET: %s" % (len(u_vertices), len(v_vertices),
                                                                               (2**len(u_vertices)-1)*(2**len(v_vertices)-1)))
        # global_tree_traverse = detect_quasi_biclique(graph, nx.subgraph(graph, vertices_in_cc))
        detect_quasi_biclique(graph, cc)
        print("End of CC")
        # break # TODO: delete after testing

    print("Quasi-bicliques in the graph: ", cluster_list)
    print("Total QBC in graph: ", len(cluster_list))
    final_time = time.time()-elapsed_time
    # print("# visits to SET: %s" % global_tree_traverse)

    print("runtime: %s" % final_time)

if __name__ == '__main__':
    get_quasi_bicliques()