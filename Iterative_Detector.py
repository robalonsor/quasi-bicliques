#!/usr/bin python3
import networkx as nx
from operator import itemgetter
import time  # Only works in Linux
import itertools
import PruneCandidates

__author__ = 'Roberto Alonso <robalonsor@gmail.com>'

# U = red
# V = blue
# SET = Set Enumeration Tree as defined in [1,2,3]

# Relative size of the QC
u_min = 5  # minimum size of the quasi-biclique
v_min = 5  # minimum size of the quasi-biclique

gamma_min = 0.5  # minimum density of the quasi-biclique
lambda_min = 0.5  # minimum density of the quasi-biclique

cluster_list = set()
debug_traversal = False
debug_traversal_u_set = False
debug_traversal_v_set = False

debug_cluster_check = True
debug_pre_processing = True

debug_traversal_visited = False # Shows the set of visited nodes in the Enum. Tree


elapsed_time = time.time()


def is_quasi_biclique(O_u, O_v, cc):
    # Checking for QBC condition w.r.t {O_u, O_v}

    min_u_edges = round(lambda_min * len(O_v))  # min. number of edges from V to U
    min_v_edges = round(gamma_min * len(O_u))  # min, num. edges from U to V
    for u in O_u:
        u_edges = 0
        for v in O_v:
            if cc.number_of_edges(u, v) >= 1:
                u_edges += 1
            if u_edges >= min_u_edges:  # reached the ideal number of edges for the vertex u
                break  # optimization, no need to check further if curr. belongs to a QBC
        if u_edges < min_u_edges:
            return False
    for v in O_v:
        v_edges = 0
        for u in O_u:
            if cc.number_of_edges(u, v) >= 1:
                v_edges += 1
            if v_edges >= min_v_edges:  # reached the ideal number of edges for vertex v
                break
        if v_edges < min_v_edges:  # if the min # of edges v is less than v_edge, v cannot be part of a QBC
            return False
    return True


def detect_quasi_biclique(graph, cc):
    global debug_traversal
    global debug_traversal_u_set
    global debug_traversal_v_set
    global debug_traversal_visited
    global debug_cluster_check

    # Sorting according to degree. Considering this order, we expand the enumeration tree
    # TODO: fix sorting. should be sorted w.r.t to degree?
    # sorted_vertices = sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)
    #
    candidates_U_root = [n for n, d in cc.nodes(data=True) if d['color'] == "red"]
    candidates_V_root = [n for n, d in cc.nodes(data=True) if d['color'] == "blue"]

    k = min(u_min, v_min)
    counter = 0 # the number of expansion conducted even if redundant
    actual_check = 0 # the real number of checked nodes
    visited = set()
    while k <= len(candidates_U_root) and k <= len(candidates_V_root):
        for c in itertools.combinations(candidates_U_root, k):
            for c_2 in itertools.combinations(candidates_V_root, k):
                print("*U-V expansion O -->  ", c, c_2) if debug_traversal else False
                counter += 1

                # Initializing candidate sets
                # candidates_U = list(set(candidates_U_root) - set(c))
                # candidates_V = list(set(candidates_V_root) - set(c_2))
                candidates_U = []
                candidates_V = []
                copy_curr_U_in_O = list(c)
                copy_curr_V_in_O = list(c_2)
                vertex_u_in_O = list(c)
                vertex_v_in_O = list(c_2)
                # Initializing this way is O(n+m) but at least we save some space compared
                # to the set approach that uses more memory but is O(1)
                # Basically we are doing candiates_set - c (i.e. candidates_in_U = U \ O_u
                i = 0
                while i < len(candidates_U_root):
                    if len(copy_curr_U_in_O) <= 0:
                        candidates_U.append(candidates_U_root[i])
                    else:
                        if candidates_U_root[i] != copy_curr_U_in_O[0]:
                            # print(c[0], candidates_U_root[i])
                            candidates_U.append(candidates_U_root[i])
                        else:
                            copy_curr_U_in_O.pop(0)
                    i += 1
                # Likewise candidates_in_V = V \ O_v
                i = 0
                while i < len(candidates_V_root):
                    if len(copy_curr_V_in_O) <= 0:
                        candidates_V.append(candidates_V_root[i])
                    else:
                        if candidates_V_root[i] != copy_curr_V_in_O[0]:
                            candidates_V.append(candidates_V_root[i])
                        else:
                            copy_curr_V_in_O.pop(0)
                    i += 1
                # the following stack is used in the U-expansion
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                # U-expansion
                U_stack = [[O[0], list(candidates_U)]]  # initialization of stack for node
                # visited = set()
                while U_stack:
                    O_u = list(U_stack[-1][0])  # set O; potential quasi-clique
                    O_u.sort()
                    candidates = list(U_stack[-1][1])  # candidates U to be part of the potential quasi-clique O
                    if (tuple(O_u), tuple(O[1])) not in visited and len(O_u) >= u_min:
                        # We have not visited current node
                        # so, we check for cluster
                        # Checking cluster
                        print("\t**(U-exp) O --> ", O_u, O[1], " candidates ->", candidates, []) if debug_traversal_u_set else False
                        actual_check += 1
                        visited.add((tuple(O_u), tuple(O[1])))
                        # If {O_u, O_v} is a potential QBC...
                        if is_quasi_biclique(O_u, O[1], cc):
                            cluster_list.add((tuple(O_u), tuple(O[1])))

                        # At this point we have checked for cluster
                    #Pruning candidate set

                    candidates = PruneCandidates.prune_candidates_u(O_u, O[1], candidates, [], cc, gamma_min, lambda_min)
                    # exit()
                    #
                    # if there are candidates, we expand

                    if len(candidates) == 0:
                        # print("\t  **(U-exp) Finally checking O set", O_u) if debug_traversal_u_set else False
                        U_stack.pop()
                        # actual_check += 1
                        continue
                    # TODO: select better vertices considering e.g. degree

                    # Expanding to the next suitable vertex (neighbor) from candidate set

                    next_neighbor = candidates.pop(0)  # getting neighbor w.r.t order in cand. set
                    U_stack[-1][1].pop(0)  # deleting, also, neighbor from curr. node in enum. tree

                    print("\t  O+u_next=", tuple(O_u + [next_neighbor])) if debug_traversal_visited else False
                    print("\t  visited=", visited) if debug_traversal_visited else False

                    # Checking that we have not expanded to this node in SET
                    while (tuple(O_u + [next_neighbor]), tuple(O[1])) in visited and len(candidates) > 0:
                        next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
                    # TODO: Apparently, there are no edge cases that activate this rule (delete?)
                    # if tuple(O_u + [next_neighbor]) in visited:
                    #     # this means len(candidates) <= 0, so add this last element to stack
                    #     print("last element")
                    #     U_stack.pop()
                    #     visited.add(tuple(O_u))
                    #     continue
                    #
                    # At this point, we know that there is at least one
                    # vertex to use in the expansion step. We expand

                    O_u.append(next_neighbor)
                    O_u.sort()
                    U_stack.append([O_u, candidates])

                    #After expanding we continue check the U_stack
                    #
                # At this point we have checked the U_stack and now we check the V_stack
                #
                # V-expansion
                #
                O = [list(vertex_u_in_O), list(vertex_v_in_O)]
                V_stack = [[O[1], list(candidates_V)]]  # initialization of stack for node
                # visited = set()
                while V_stack:
                    O_v = list(V_stack[-1][0])  # set O; potential quasi-clique
                    O_v.sort()
                    # if time.time()-elapsed_time > 100:
                    #     print("Killing... taking more than 300 seconds")
                    #     return
                    candidates = list(V_stack[-1][1])  # candidates to be part of the potential quasi-clique O
                    if (tuple(O[0]), tuple(O_v)) not in visited and len(O_v) >= v_min:
                        print("\t++(V-exp) O --> ", O[0], O_v, " candidates ->", [], candidates) if debug_traversal_v_set else False
                        visited.add((tuple(O[0]), tuple(O_v)))
                        actual_check += 1
                        if is_quasi_biclique(O[0], O_v, cc):
                            cluster_list.add((tuple(O[0]), tuple(O_v)))
                    # Pruning candidates

                    candidates = PruneCandidates.prune_candidates_v(O[0], O_v, [], candidates, cc, gamma_min,
                                                                    lambda_min)
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

        k += 1
        # break
    # print(visited)
    print("# of U-V expansions:  %s - # of visits to SET:  %s" % (counter, actual_check))


def pre_processing(graph):
    global debug_pre_processing
    vertices_to_remove = []
    min_u_edges = round(lambda_min * v_min)  # min. number of edges from V to U
    min_v_edges = round(gamma_min * u_min) # min, num. edges from U to V
    # print(min_u_edges, min_v_edges)
    if debug_pre_processing:
        u_before = len([n for n, d in graph.nodes_iter(data=True) if d['color'] == 'red'])
        v_before = len([n for n, d in graph.nodes_iter(data=True) if d['color'] == 'blue'])
        print("Before pre-processing. |U| = %s  |V| = %s" % (u_before, v_before)) if debug_pre_processing else False
    keep_cleaning = True
    while keep_cleaning:
        keep_cleaning = False
        for n, d in graph.nodes_iter(data=True): # iterating trough vertices in graph
            # for all u in U if |E(u)| < gamma X u_min. then not possible to be QBC
            if d['color'] == 'red' and min_u_edges > graph.degree(n):  # U
                vertices_to_remove.append(n)
                keep_cleaning = True
                continue
            # likewise for all v in V if |E(v)| < lambda X v_min. not a QBC
            if d['color'] == 'blue' and min_v_edges > graph.degree(n):
                vertices_to_remove.append(n)
                keep_cleaning = True
        # Removing vertices from graph
        graph.remove_nodes_from(vertices_to_remove)
        # Ater this point we have safely deleted vertices that won't form a QBC
        # print([str(n) +" "+ str(graph.degree(n)) for n, d in graph.nodes_iter(data=True)])
    if debug_pre_processing:
        u_after = len([n for n, d in graph.nodes_iter(data=True) if d['color'] == 'red'])
        v_after = len([n for n, d in graph.nodes_iter(data=True) if d['color'] == 'blue'])
        print("After pre-processing.  |U| = %s  |V| = %s" % (u_after, v_after)) if debug_pre_processing else False


def get_quasi_bicliques():
    pre_processing_flag = False

    # graph = nx.read_graphml('datasets/toy_bipartite.graphml', node_type=int)
    # graph = nx.read_graphml('datasets/bipartite.graphml', node_type=int)
    graph = nx.read_graphml('datasets/amazon_thousands.graphml', node_type=int)

    print("Looking for quasi bicliques with gamma <%s> density; lambda <%s> density "
          "and min. size of U = <%s> and V = <%s>"% (gamma_min, lambda_min, u_min, v_min))
    if not nx.is_bipartite(graph):
        print("Not a bipartite graph")
        return
    # elapsed_time = time.time()  # Starting timer
    print("Warning! Graph pre-processing disabled\n") if not pre_processing_flag else pre_processing(graph)
    pre_processing(graph) # Passing by reference?

    # After this point, the graph contains a cleaned version of the graph

    cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
    # Iterating through connected components

    for cc in cc_list:
        if not nx.is_bipartite(cc):
            continue
        u_vertices = set(n for n, d in cc.nodes(data=True) if d['color'] == "red")
        v_vertices = set(n for n, d in cc.nodes(data=True) if d['color'] == "blue")

        if len(v_vertices) < v_min or len(u_vertices) < u_min:
            print("skipping CC.  |U'| = %s  |V'| = %s" % (len(u_vertices), len(v_vertices)))
            continue
        print("CC of # vertices: |U| = %s ,  |V| = %s   total nodes SET: %s" % (len(u_vertices), len(v_vertices),
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