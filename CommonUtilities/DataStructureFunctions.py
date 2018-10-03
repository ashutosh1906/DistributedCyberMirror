def delete_values_by_index_from_list(data_structure,delete_index):
    ''' This fundtion will remove the values of the corresponding indexs of "delete_index" list'''
    '''data structure is the original list'''
    number_values_removed = 0
    for i in delete_index:
        del data_structure[i - number_values_removed]
        number_values_removed += 1

def normalization_by_min(data_structure):
    '''Normalize each value by in the minimum element to get the ratio'''
    min_value = min(data_structure)
    length_list = len(data_structure)
    for index in range(len(data_structure)):
        data_structure[index] /= min_value