#!/usr/bin python3
import networkx as nx
from operator import itemgetter
import time  # Only works in Linux

u_min = 4
# Relative size of the QC
g_min = 0.5  # gamma min

cluster_list = []

def quasi_clique(cc):
    sorted_vertices = sorted(graph.degree_iter(), key=itemgetter(1), reverse=True)
    # vertex = sorted_vertices.pop(0)[0]
    # candidates_root = list(nx.to_dict_of_lists(cc).keys())
    candidates_root = [x[0] for x in sorted_vertices]
    counter_debug = 0
    tree_traversal = 0
    visited = set()

    while len(candidates_root) > 0:
        tree_traversal += 1
        candidates = list(candidates_root)
        vertex = candidates.pop(0)
        # candidates.pop(candidates.index(vertex))
        stack = [[[vertex], candidates]]  # initialization of stack for root node

        while stack:
            # if counter_debug >= 33:
            #     break
            counter_debug += 1
            # process the candidates
            O = list(stack[-1][0])
            candidates = list(stack[-1][1])
            # print("O --> ", O, " candidates ->", candidates)
            v_min_edges = round(len(O) * g_min, 0)  # all u in U must have these min number of edges to be a QBC

            try:
                if tuple(O) in visited:
                    raise Exception("Already checked density. Pruning stage...")
                if len(O) <= u_min:
                    raise Exception("|O| < gamma_min")
                if v_min_edges == 0:  # root nodes
                    raise Exception("Root nodes. Expanding if possible")
                if len(candidates) <= 0:
                    raise Exception("No moro candidates to prune")

                # Diameter prunning
                max_diameter = 2
                intersection_of_vertices = set()
                for vertex in O:
                    neighbors_of_v = nx.single_source_shortest_path(cc, vertex, max_diameter)
                    #print("neigh..", neighbors_of_v, " v = ", vertex)
                    if intersection_of_vertices:
                        # compute new intersection of vertices
                        intersection_of_vertices = intersection_of_vertices.intersection(neighbors_of_v)
                    else:
                        intersection_of_vertices = set(neighbors_of_v.keys())

                candidates = [item for item in candidates if item in intersection_of_vertices]

                    # prune candidates that doesn't have |O|*g_min degree (v_min_degree)
                    # u_edges_to_v = 0
                    # for i in range(0,len(candidates)):
                    #     for j in range(i,len(candidates)):
                    #         if cc.number_of_edges(candidates[i], candidates[j]) >= 1:
                    #             u_edges_to_v += 1
                    #         if u_edges_to_v >= v_min_edges:  # reached the ideal number of edges for the vertex u
                    #             break  # optimization, no need to check further if curr. belongs to a QC
                    # prune candidates based on diameter
            except Exception as er:
                # print("\t Exception: ", er, "!!!!")
                pass
            finally:
                try:
                    if len(O) >= u_min:
                        # checking for QC
                        u_edges_to_v = 0
                        for i in range(0, len(O)):
                            for j in range(i, len(O)):
                                if cc.number_of_edges(O[i], O[j]) >= 1:
                                    u_edges_to_v += 1
                                if u_edges_to_v >= v_min_edges:
                                    continue
                            if u_edges_to_v < v_min_edges:
                                # it is not a QC
                                raise Exception("O = ", O, " is not a quasi-clique")
                        cluster_list.append(list(O)) if O not in cluster_list else ""
                        # print("*****", O)
                except Exception as er:
                    # print("\t\t Exception: ", er, "!!!!")
                    pass
            # choosing next neighbor
            # delete from stack if no further expansion possible
            if len(candidates) == 0:
                # print("Candidate set empty")
                stack.pop()
                visited.add(tuple(O))
                # print(visited)
                continue
            next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
            while tuple(O + [next_neighbor]) in visited and len(candidates) > 0:
                next_neighbor = candidates.pop(0)  # sorted_vertices.pop(0)[0]
            if tuple(O + [next_neighbor]) in visited:
                # print("Already visited", O + [next_neighbor], "Adding O to visits O= ", O, "cand = ", candidates)
                stack.pop()
                visited.add(tuple(O))
                continue
            # expansion of Enum. Tree
            tree_traversal += 1
            O.append(next_neighbor)
            stack.append([O, candidates])
        candidates_root.pop(candidates_root.index(O[0]))
        # print("Re-starting considering V = ", candidates_root)

    return tree_traversal


graph = nx.read_graphml('datasets/V_c10.graphml', node_type=int)
# Pre-processing graph
# every vertex in G must have at least u_min*g_min edges, otherwise no quasi-clique
for v in graph.copy():
    if graph.degree(v) == 0:  # u_min_edges:
        graph.remove_node(v)

cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
# Iterating through connected components
# elapsed_time = time.clock() # Starting timer
elapsed_time = time.clock() # Starting timer
for cc_index in range(len(cc_list)):
    vertices_in_cc = set(cc_list[cc_index].nodes())
    if len(vertices_in_cc) < u_min:
        continue
    print("CC: ", vertices_in_cc)
    print(quasi_clique(nx.subgraph(graph, vertices_in_cc)))
    print("End of CC")
    break

print("Quasi-cliques in the graph: ", cluster_list)
final_time = time.clock()-elapsed_time
print("runtime: %s" % final_time)
