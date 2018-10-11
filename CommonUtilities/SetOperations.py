def combination_possible_values_all_positions(data_structure):
    ''' Return all the possible combinations among the nodes where each node has a set of distinct values'''
    ''' arg:data_structure is a 2-dimensional list where for each index of arg:data_structure, there will be a list of possible values'''
    '''In the return value, for each index of arg:data_structure, there will be a possible value from its corresponding list of values'''
    '''The return value will contain all the possible combinations where each combination will be a list'''
    possible_combinations = []
    # print('!!!! --> Data Structure %s <--- !!!!'%(data_structure))
    __iteration_over_possible_combinations(data_structure,[],possible_combinations)
    return possible_combinations


def __iteration_over_possible_combinations(data_structure,chosen_node,possible_combinations):
    # print('!!!! --> Data Structure %s <--- !!!!' % (data_structure))
    if len(data_structure)==0:
        create_list = []
        for value in chosen_node:
            create_list.append(value)
        possible_combinations.append(create_list)
        return
    current_type = data_structure[0]
    for value in current_type:
        chosen_node.append(value)
        __iteration_over_possible_combinations(data_structure[1:],chosen_node,possible_combinations)
        del chosen_node[-1]

def iteration_over_possible_combinations_no_duplicate(data_structure,chosen_node,possible_combinations):
    if len(data_structure)==0:
        create_list = []
        for num in chosen_node:
            create_list.append(num)
        possible_combinations.append(create_list)
        return
    current_type = data_structure[0]
    for value in current_type:
        if value not in chosen_node:
            chosen_node.add(value)
            iteration_over_possible_combinations_no_duplicate(data_structure[1:], chosen_node, possible_combinations)
            chosen_node.remove(value)
        else:
            iteration_over_possible_combinations_no_duplicate(data_structure[1:], chosen_node, possible_combinations)

def iteration_over_possible_combinations_list_based(data_structure,chosen_node,possible_combinations):
    # print('List based Iterations %s'%(data_structure))
    if len(data_structure)==0:
        create_list = []
        for value in chosen_node:
            create_list.append(value)
        possible_combinations.append(create_list)
        return
    current_type = data_structure[0]
    for value in current_type:
        chosen_node.append(value)
        iteration_over_possible_combinations_list_based(data_structure[1:],chosen_node,possible_combinations)
        del chosen_node[-1]

def merge_lists(given_list,elements):
    # print('Merge %s'%(given_list))
    for value in given_list:
        if type(value)==list:
            merge_lists(value, elements)
        else:
            elements.append(value)