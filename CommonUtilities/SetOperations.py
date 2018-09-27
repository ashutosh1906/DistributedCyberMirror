def combination_possible_values_all_positions(data_structure):
    ''' Return all the possible combinations among the nodes where each node has a set of distinct values'''
    ''' arg:data_structure is a 2-dimensional list where for each index of arg:data_structure, there will be a list of possible values'''
    '''In the return value, for each index of arg:data_structure, there will be a possible value from its corresponding list of values'''
    '''The return value will contain all the possible combinations'''
    possible_combinations = []
    # print('!!!! --> Data Structure %s <--- !!!!'%(data_structure))
    __iteration_over_possible_combinations(data_structure,possible_combinations)


def __iteration_over_possible_combinations(data_structure,possible_combinations):
    # print('!!!! --> Data Structure %s <--- !!!!' % (data_structure))
    