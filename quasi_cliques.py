#!/usr/bin python3
import networkx as nx
from operator import itemgetter
import time  # Only works in Linux

__author__ = 'Roberto Alonso <robalonsor@gmail.com>'

# Inspired in the work of
# [1] Abello
# [2] Liu
# [3] Gunnemann

# Relative size of the QC
v_min = 6  # minimum size of the quasi-clique
g_min = 0.7  # minimum density of the quasi-clique

debug_prun = False
debug_traversal = False
debug_exceptions = False
global_tree_traverse = 0
cluster_list = set()#[]  # using a list means that every time we want to insert cluster, we check if not already there
                  # a potential workaround is to use a set


def detect_quasi_clique(graph, cc):
    # Sorting according to degree. Considering this order, we expand the enumeration tree
    sorted_vertices = sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)
    candidates_root = [x[0] for x in sorted_vertices]
    counter_debug = 0
    tree_traversal = 0
    visited = set()

    while len(candidates_root) > 0:
        tree_traversal += 1
        candidates = list(candidates_root)
        vertex = candidates.pop(0)
        # candidates.pop(candidates.index(vertex))
        stack = [[[vertex], candidates]]  # initialization of stack for root (empty) node
        # Note: for the sake of simplicity, each parent node with |O| = 1 is
        # called root_node. However, mathematically the root node in the enumeration tree
        # is the empty node. See e.g. [2,3]
        while stack:
            counter_debug += 1

            O = list(stack[-1][0])  # set O; potential quasi-clique
            candidates = list(stack[-1][1])  # candidates to be part of the potential quasi-clique O
            print("O --> ", O, " candidates ->", candidates) if debug_traversal else False
            v_min_edges = round(len(O) * g_min, 0)  # all v in {O+cand} must have ceil(|O|*\gamma_min) edges; otherwise
                                                    # not it is not possible to form a quasi-clique

            try:
                if len(O) <= v_min:
                    raise Exception("|O| < gamma_min")
                if v_min_edges == 0:  # root nodes
                    raise Exception("Root nodes. Expanding if possible")
                if len(candidates) <= 0:
                    raise Exception("No moro candidates to prune")
                # TODO: Unit testing on pruning techniques
                # Pruning candidate set
                keep_pruning = True

                while keep_pruning:
                    keep_pruning = False
                    # Degree pruning
                    cand_to_remove = set()
                    for v1 in candidates:
                        out_edges = 0
                        if v1 in cand_to_remove:
                            continue
                        for v2 in candidates:
                            if v2 in cand_to_remove or v1 == v2:
                                continue
                            if cc.number_of_edges(v1, v2) >= 1:
                                out_edges += 1
                            if out_edges >= v_min_edges:
                                # no need to check further edges
                                break
                        if out_edges < v_min_edges:
                            cand_to_remove.add(v1)
                    if len(cand_to_remove) > 0:
                        print("We have pruned with Degree", cand_to_remove) if debug_prun else False
                        for v in cand_to_remove:
                            candidates.pop(candidates.index(v))
                        keep_pruning = True
                    # Diameter pruning
                    max_diameter = 2
                    intersection_of_vertices = set()
                    for vertex in O:
                        neighbors_of_v = nx.single_source_shortest_path(cc, vertex, max_diameter)
                        if intersection_of_vertices:
                            intersection_of_vertices = intersection_of_vertices.intersection(neighbors_of_v)
                        else:
                            intersection_of_vertices = set(neighbors_of_v.keys())
                    len_cand = len(candidates)
                    # print("Diam->", candidates)
                    candidates = [item for item in candidates if item in intersection_of_vertices]
                    # print("Diam->", candidates)
                    if len_cand != len(candidates):  # if there was any change in candidate set, keep_pruning
                        print("We have pruned with Diameter") if debug_prun else False
                        keep_pruning = True

                # if tuple(O) in visited:
                #     raise Exception("Already checked density. Pruning stage...")
            except Exception as er:
                print("\t Exception: ", er, "!!!!") if debug_exceptions else False
                pass
            finally:
                try:
                    # if tuple(O) in visited:
                    #     raise Exception("Already checked density. Quasi-clique stage...")
                    if len(O) >= v_min:
                        # checking for QC
                        sorted_O = O.copy()
                        sorted_O.sort()

                        if tuple(sorted_O) in cluster_list:
                            raise Exception("O is a cluster")  # no need to check
                        for v1 in O:
                            v1_edges_to_v2 = 0
                            for v2 in O:
                                if v1 == v2:
                                    continue
                                if v1_edges_to_v2 >= v_min_edges:
                                    break
                                if cc.number_of_edges(v1, v2) >= 1:
                                    v1_edges_to_v2 += 1
                            if v1_edges_to_v2 < v_min_edges:
                                # it is not a QC
                                raise Exception("O = ", O, " is not a quasi-clique min edges = ", v_min_edges)
                        #cluster_list.append(list(O)) if O not in cluster_list else ""
                        cluster_list.add(tuple(sorted_O))
                        # print("*")
                except Exception as er:
                    print("\t\t Exception: ", er, "!!!!") if debug_exceptions else False
                    pass
            # choosing next neighbor
            # delete from stack if no further expansion possible
            # then, continue to the next node in the enumerationt tree
            if len(candidates) == 0:
                stack.pop()
                visited.add(tuple(O))
                continue
            # TODO: make sure next_neighbor is connected to set O
            # Expanding to the next suitable vertex
            next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
            stack[-1][1].pop(0)  # deleting from curr. node in enum. tree

            while tuple(O + [next_neighbor]) in visited and len(candidates) > 0:
                next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
            if tuple(O + [next_neighbor]) in visited:
                # print("Already visited", O + [next_neighbor], "Adding O to visits O= ", O, "cand = ", candidates)
                stack.pop()
                visited.add(tuple(O))
                continue
            # At this point, we know that there is at least one
            # vertex to use in the expansion step. We expand
            tree_traversal += 1
            O.append(next_neighbor)
            stack.append([O, candidates])

            visited.add(tuple(stack[-1][0]))

        candidates_root.pop(candidates_root.index(O[0]))
        # print("Re-starting considering V = ", candidates_root)

    return tree_traversal


def get_quasi_cliques():
    global global_tree_traverse
    graph = nx.read_graphml('datasets/V_c10.graphml', node_type=int)
    # graph = nx.read_graphml('datasets/toy.graphml', node_type=int)
    # Pre-processing graph
    # every vertex in G must have at least u_min*g_min edges, otherwise no quasi-clique

    # for v in graph.copy():
    #     if graph.degree(v) == 0:  # u_min_edges:
    #         graph.remove_node(v)
    print("Looking for quasi cliques with gamma <%s> density and min. size of <%s> "% (g_min,v_min))
    elapsed_time = time.time()  # Starting timer
    # pre-processing graph
    # A vertex in G forms a quasi-clique if and only if
    # its degree is at least ceil(v_min*gamma_min)
    keep_pruning = True
    while keep_pruning:
        keep_pruning = False
        for v_degree in graph.copy().degree_iter():
            deg = v_degree[1]
            if deg < round(v_min*g_min):
                keep_pruning = True
                graph.remove_node(v_degree[0])
                # print("xx")

    cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
    # Iterating through connected components
    global_tree_traverse = 0
    for cc_index in range(len(cc_list)):
        vertices_in_cc = set(cc_list[cc_index].nodes())
        if len(vertices_in_cc) < v_min:
            continue
        print("CC of # vertices: ", len(vertices_in_cc))
        global_tree_traverse = detect_quasi_clique(graph, nx.subgraph(graph, vertices_in_cc))
        print("End of CC")
        break

    print("Quasi-cliques in the graph: ", cluster_list)
    print("Total QC in graph: ", len(cluster_list))
    final_time = time.time()-elapsed_time
    print("# visits to SET: %s" % global_tree_traverse)

    print("runtime: %s" % final_time)

get_quasi_cliques()