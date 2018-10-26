from CommonUtilities import SetOperations

def graph_traversal_concurrent(data_structure):
    '''Start the journey from one or more points towards a destination. Each content of the data structure is path where
    path[0]=start_node and path[-1]=destination. This functions computes all the possible combinations of concurrent nodes
    when the agent can move one step at each time. For example, [1,2,4] means the possible nodes are 1,2,4 and [3] means that this is the only possible node.
    arg:data_structure is a list which contains paths (represented as list) from the start point to destination.
    Output: return the list of all combinations of possible nodes
    For Example, if data_structure is [[2,1],[3,1]], then the output is [[2,3],[1]] (We ignore a node if its ancestor is present in the combination. Root is
    ancestor of all the nodes except itself)'''
    print('***** Given Data Structure %s **********'%(data_structure))

    sent_data_structure = []
    for data in data_structure:
        sent_data_structure.append(data[:-1])
    possible_combinations = path_traversal_from_root(sent_data_structure)
    # print('Possible Combinations %s'%(possible_combinations))
    #### Add Root ##############
    possible_combinations.append([data_structure[0][-1]])
    # print('Possible Combinations %s' % (possible_combinations))

    original_combinations = []
    for value in possible_combinations:
        get_position_concurrent = []
        SetOperations.merge_lists(value,get_position_concurrent)
        original_combinations.append(get_position_concurrent)
    return original_combinations

def path_traversal_from_root(data_structure):
    # print('DS %s'%(data_structure))
    if len(data_structure)==1:
        child_combination = []
        for data in data_structure[0]:
            child_combination.append([data])
        # print('Child %s'%(child_combination))
        return child_combination

    subtree_data_structure = {}
    path_index = 0
    for path in data_structure:
        if len(path)==0:
            continue
        if path[-1] not in subtree_data_structure:
            subtree_data_structure[path[-1]] = [path_index]
        else:
            subtree_data_structure[path[-1]].append(path_index)
        path_index += 1

    # print('Subtree %s --> %s' % ('T', subtree_data_structure))
    if len(subtree_data_structure)==1:
        sent_data_structure = []
        for data in data_structure:
            sent_data_structure.append(data[:-1])
        child_combination = path_traversal_from_root(sent_data_structure)
        for key in subtree_data_structure:
            child_combination.append([key])
        # print('Combinations %s --> %s' % ('C',child_combination))
        return child_combination

    elif len(data_structure)==len(subtree_data_structure):
        child_combination = []
        SetOperations.iteration_over_possible_combinations_no_duplicate(data_structure,set({}),child_combination)
        # print("CTC %s --> %s"%(last_index_to_read,possible_combinations))
        return child_combination

    else:
        key_index = 0
        child_tree_combinations = []
        for key in subtree_data_structure:
            sent_data_structure = []
            for path_index in subtree_data_structure[key]:
                sent_data_structure.append(data_structure[path_index][:-1])
            print('Sent Data Structure %s'%(sent_data_structure))
            child_tree_combinations.append(path_traversal_from_root(sent_data_structure))
            child_tree_combinations[key_index].append([key])
            # print("CTC %s of key:%s --> %s" % ('CTC',key,child_tree_combinations[key_index]))
            key_index += 1
        # print('Create Data Structure %s'%(child_tree_combinations))
        child_combination = []
        SetOperations.iteration_over_possible_combinations_list_based(child_tree_combinations,[],child_combination)
        return child_combination

def determine_descendents(data_structure):
    '''Determine descendents from the given paths.
    Each content of the data structure is a path'''
    descendant_nodes = {}
    for path in data_structure:
        path_length = len(path)
        for element_index in range(path_length-1,-1,-1):
            element = path[element_index]
            if element not in descendant_nodes:
                descendant_nodes[element] = set(path[0:element_index])
            else:
                descendant_nodes[element] |= set(path[0:element_index])
    print(descendant_nodes)
