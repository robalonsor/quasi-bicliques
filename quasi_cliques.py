#!/usr/bin python3
__author__ = 'Roberto Alonso <robalonsor@gmail.com>'

# Inspired in the work of
# [1] Abello
# [2] Liu
# [3] Gunnemann

# Relative size of the QC
v_min = 5  # minimum size of the quasi-clique
g_min = 0.6  # minimum density of the quasi-clique

debug_prun = False
debug_traversal = False
debug_exceptions = False
debug_cluster = False
sentinel = -1


def detect_quasi_clique(q, g, cc, r_queue):
    # Sorting according to degree. Considering this order, we expand the enumeration tree
    global counter_debug
    global visited
    global tree_traversal
    cluster_list = set()
    #sorted_vertices = sorted(g.degree_iter(), key=itemgetter(1), reverse=True)
    tree_traversal += 1

    while True:
        O_cand = q.get()
        O = [O_cand[0]]
        candidates = O_cand[1]
        if len(candidates) <= 0:
            assert len(O) == 1
            # q.task_done()
            return 1

        #vertex = candidates.pop(0)
        # candidates.pop(candidates.index(vertex))
        stack = [[O, candidates]]  # initialization of stack for root (empty) node
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
                # if tuple(O) in visited:
                #     raise Exception("Already checked density. Pruning stage...")
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
                    len_cand = len(candidates.copy())
                    # print("Diam->", candidates)
                    candidates = [item for item in candidates if item in intersection_of_vertices]
                    # print("Diam->", candidates)
                    if len_cand != len(candidates):  # if there was any change in candidate set, keep_pruning
                        print("We have pruned with Diameter") if debug_prun else False
                        keep_pruning = True
            except Exception as er:
                print("\t Exception: ", er, "!!!!") if debug_exceptions else False
                pass
            finally:
                try:
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
                        # cluster_list.append(list(O)) if O not in cluster_list else ""
                        cluster_list.add(tuple(sorted_O))
                        print("adding v= ", sorted_O) if debug_cluster else False
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
        # at this point there is nothing left in the stack
        break

    r_queue.put(cluster_list) if len(cluster_list) > 0 else False


def create_queue(q, cc):
    from operator import itemgetter
    sorted_vertices = sorted(cc.degree_iter(), key=itemgetter(1), reverse=True)
    list_of_vertices = [item[0] for item in sorted_vertices]

    while len(list_of_vertices) > 0:
        O = list_of_vertices.pop(0)
        candidates = list(list_of_vertices)
        q.put([O, candidates])

if __name__ == '__main__':
    import networkx as nx
    import time  # Only works in Linux
    from multiprocessing import Process, Queue
    import os
    os.system("taskset -p 0xff %d" % os.getpid())

    counter_debug = 0
    tree_traversal = 0
    visited = set()
    final_result = []
    # cluster_list = set()  # []  # using a list means that every time we want to insert cluster, we check if not already there
    # a potential workaround is to use a set
    graph = nx.read_graphml('datasets/V_c10.graphml', node_type=int)
    # graph = nx.read_graphml('datasets/toy.graphml', node_type=int)
    elapsed_time = time.time()  # Starting timer

    # Pre-processing graph
    # every vertex in G must have at least u_min*g_min edges, otherwise no quasi-clique
    print("Looking for quasi cliques with gamma <%s> density and min. size of <%s> " % (g_min, v_min))
    # pre-processing graph
    # A vertex in G forms a quasi-clique if and only if
    # its degree is at least ceil(v_min*gamma_min)
    # print(nx.number_of_nodes(graph))
    keep_pruning = True
    while keep_pruning:
        keep_pruning = False
        for v_degree in graph.copy().degree_iter():
            deg = v_degree[1]
            if deg < round(v_min * g_min):
                keep_pruning = True
                graph.remove_node(v_degree[0])

    cc_list = list(nx.connected_component_subgraphs(graph))  ## list of connected components
    # Iterating through connected components
    print(cc_list[0])
    for cc_index in range(len(cc_list)):
        vertices_in_cc = set(cc_list[cc_index].nodes())
        if len(vertices_in_cc) < v_min:
            continue
        print("CC of # vertices: ", len(vertices_in_cc))

        q = Queue()  # Queue(maxsize=0)
        result_queue = Queue()
        num_processes = 1
        jobs = []
        connected_component = nx.subgraph(graph, vertices_in_cc)
        creator_process = Process(target=create_queue, args=(q, connected_component))

        for item in range(num_processes):
            detector_process = Process(target=detect_quasi_clique, args=(q, graph, connected_component, result_queue))
            jobs.append(detector_process)

        creator_process.start()

        for job in jobs: job.start()
        q.close()
        q.join_thread()
        creator_process.join()
        for job in jobs: job.join()

        results = [result_queue.get() for i in range(num_processes)]
        final_result.append(results)
        visited = set()  # Reset visited nodes of enumeration tree
        print("End of CC")

    print("Quasi-cliques in the graph: ", final_result)
    # print("Total QC in graph: ", len(cluster_list))
    final_time = time.time()-elapsed_time
    print("# visits to SET: %s" % tree_traversal)
    print("runtime: %s" % final_time)