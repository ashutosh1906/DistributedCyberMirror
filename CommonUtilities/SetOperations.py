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
