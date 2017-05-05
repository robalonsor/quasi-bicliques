#!/usr/bin python3

import networkx as nx
import numpy as np

def prune_candidates_u(O_u, O_v, candidates_U, candidates_V, cc, gamma_min, lambda_min):
    debug_output = False
    if len(candidates_U) <= 0:
        print("++ There is nothing to prune. Returning.") if debug_output else False
        return candidates_U

    # Storing in a dict function calls
    dict_of_prun_tech = {'degree': prune_based_on_degree, 'diameter': prune_based_on_diameter}
    # dict_of_prun_tech = {'degree': prune_based_on_degree}
    # dict_of_prun_tech = {'diameter': prune_based_on_diameter}

    # For each pruning technique (defined in dictionary and in module), prune candidates
    
    # G.remove_nodes_from([ n in G if n not in set(nbunch)])
    # cc_subgraph = nx.Graph(cc)
    # cc_subgraph.remove_nodes_from([n for n in cc if n not in O_u + O_v + candidates_U + candidates_V])

    to_extract = np.array(O_u + O_v + candidates_U + candidates_V)
    A = nx.to_scipy_sparse_matrix(cc, format='lil')
    print(A)
    exit()
    A_sub = A[to_extract, to_extract].copy()
    cc_subgraph = nx.Graph(A_sub)

    # cc_subgraph = cc.subgraph(O_u + O_v + candidates_U + candidates_V)
    print("\n*-Starting all pruning techniques.-*\n") if debug_output else False
    repeat = True
    first_time = True
    while repeat:
        repeat = False
        for prun_technique in dict_of_prun_tech.values():
            candidates_U, repeat = prun_technique(O_u, O_v, candidates_U, candidates_V, cc_subgraph, gamma_min,
                                                        lambda_min, type="u", debug=debug_output)

            if len(candidates_U) <= 0:
                print("++ After prun. tech. Nothing else to prune") if debug_output else False
                return candidates_U
            if not repeat and not first_time:
                # Watch for this rule since applying more than two technique might cuase problems in the future
                # TODO: Keep in mind the above comment
                print("++ Prev. prun. tech. Didn't modify anything, so skipping") if debug_output else False#
                break
        first_time = False

        if debug_output:
            print("****No more candidate pruning for the node in enumeration tree****")
            print("After prun.tech., cand sets are", candidates_U, candidates_V)
        print("<> Repeating pruning techniques. ") if repeat and debug_output else False

    candidates_U.sort()
    # candidates_V.sort()
    return candidates_U


def prune_candidates_v(O_u, O_v, candidates_U, candidates_V, cc, gamma_min, lambda_min):
    debug_output = False
    if len(candidates_V) <= 0:
        print("++ There is nothing to prune in V. Returning.") if debug_output else False
        return candidates_V

    # Storing in a dict function calls
    dict_of_prun_tech = {'degree': prune_based_on_degree, 'diameter': prune_based_on_diameter}

    # For each pruning technique (defined in dictionary and in module), prune candidates
    # cc_subgraph = nx.Graph(cc)
    # cc_subgraph.remove_nodes_from([n for n in cc if n not in O_u + O_v + candidates_U + candidates_V])

    cc_subgraph = cc.subgraph(O_u + O_v + candidates_U + candidates_V)
    print("\n*-Starting all pruning techniques.-*\n") if debug_output else False
    repeat = True
    first_time = True
    while repeat:
        repeat = False
        for prun_technique in dict_of_prun_tech.values():
            candidates_V, repeat = prun_technique(O_u, O_v, candidates_U, candidates_V, cc_subgraph, gamma_min,
                                                  lambda_min, type="v", debug=debug_output)

            if len(candidates_V) <= 0:
                print("++ After prun. tech. Nothing else to prune") if debug_output else False
                return candidates_V
            if not repeat and not first_time:
                # Watch for this rule since applying more than two technique might cuase problems in the future
                # TODO: Keep in mind the above comment
                print("++ Prev. prun. tech. Didn't modify anything, so skipping") if debug_output else False#
                break
        first_time = False

        if debug_output:
            print("****No more candidate pruning for the node in enumeration tree****")
            print("After prun.tech., cand sets are", candidates_U, candidates_V)
        print("<> Repeating pruning techniques. ") if repeat and debug_output else False

    candidates_V.sort()
    return candidates_V


def prune_based_on_degree(U, V, candidates_U, candidates_V, cc_subgraph, gamma_min, lambda_min, type="None", debug=False):
    repeat = False # If we delete something with curr. tech. we should apply other techniques
    if debug:
        print("~~Starting pruning <<%s>> based on degree" % type)
        print("U = ", U, "V = ", V, "cand_u = ", candidates_U, "cand_v = ", candidates_V)

    min_edges_u = round((len(V)) * lambda_min, 0)
    min_edges_v = round((len(U)) * gamma_min, 0)  # all v in candidates_V must have these edges
    if debug:
        print("min edges for u = ", min_edges_u, " and for v = ", min_edges_v)

    keep_pruning = True
    while keep_pruning:
        keep_pruning = False
        if type == "u":
            for u in candidates_U:
                if cc_subgraph.degree(u) < min_edges_u:
                    cc_subgraph.remove_node(u)
                    # print("deleting....",candidates_U.pop(candidates_U.index(u)))
                    candidates_U.pop(candidates_U.index(u))
                    keep_pruning = True
                    repeat = True
                    break
        elif type == "v":
            for v in candidates_V:
                if cc_subgraph.degree(v) < min_edges_v:
                    cc_subgraph.remove_node(v)
                    # print("deleting...", candidates_V.pop(candidates_V.index(v)))
                    candidates_V.pop(candidates_V.index(v))
                    keep_pruning = True
                    repeat = True
                    break
        else:
            print("Error while pruning vertices")
            return False
    if debug:
        print("Deg. prun. tech. Candidates after prun: ",candidates_U,candidates_V)

    if type == "u":
        return candidates_U, repeat
    return candidates_V, repeat
    # return candidates_U, candidates_V, False


def prune_based_on_diameter(U, V, candidates_U, candidates_V, cc_subgraph, gamma_min, lambda_min, type="None", debug=False):
    repeat = False
    if type == "None":
        return False
    if debug:
        print("~~Starting pruning <<%s>> based on diameter" % type)
        print(U, V, candidates_U, candidates_V)

    max_diameter = 4
    intersection_of_vertices = set()
    for vertex in U+V:
        neighbors_of_v = nx.single_source_shortest_path(cc_subgraph, vertex, max_diameter)
        if intersection_of_vertices:
            # compute new intersection of vertices
            intersection_of_vertices = intersection_of_vertices.intersection(neighbors_of_v)
        else:
            intersection_of_vertices = set(neighbors_of_v.keys())
    if debug:
        print("After computing diameter the intersection of vertices is: ")
        print(intersection_of_vertices)
        print("Deleting candidates not in the intersection")
        print("Current candidates", candidates_U, candidates_V)
    if type == "u":
        copy_candidates_U = list(candidates_U)
        candidates_U = [item for item in candidates_U if item in intersection_of_vertices]
        if candidates_U != copy_candidates_U:
            repeat = True
    elif type == "v":
        copy_candidates_V = list(candidates_V)
        candidates_V = [item for item in candidates_V if item in intersection_of_vertices]
        if candidates_V != copy_candidates_V:
            repeat = True
    if debug:
        print("Diam. After diam. prun. candidates are: ", candidates_U, candidates_V)

    if type == "u":
        return candidates_U, repeat
    return candidates_V, repeat


def prune_vertices(O_u, O_v, candidates_U, candidates_V, cc, gamma_min, lambda_min):
    debug_output = True
    # Storing in a dict function calls
    dict_of_prun_tech = {'degree': prune_based_on_degree, 'diameter': prune_based_on_diameter}

    fail_flag = False
    # For each pruning technique (defined in dictionary and in module), prune candidates
    cc_subgraph = cc.subgraph(O_u+O_v+candidates_U+candidates_V)
    if min(list(cc_subgraph.degree().values())) <= 0:
        print("U+V and candidatesU+candidatesV are a disconnected graph") if debug_output else False
        # return candidates_U, candidates_V, True
        return []

    for prun_technique in dict_of_prun_tech.values():
        candidates_U, candidates_V = prun_technique(O_u, O_v, candidates_U, candidates_V, cc_subgraph, gamma_min, lambda_min, debug_output)

    if debug_output:
        print("****No more candidate pruning for the node in enumeration tree****")
        print("After prun.tech., cand sets are", candidates_U, candidates_V)

    candidates_U.sort()
    candidates_V.sort()

    return candidates_U, candidates_V, fail_flag

def main():
    pass

if __name__ == "__main__":
    main()