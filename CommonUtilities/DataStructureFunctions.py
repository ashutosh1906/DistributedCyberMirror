from operator import itemgetter, attrgetter

def delete_values_by_index_from_list(data_structure,delete_index):
    ''' This fundtion will remove the values of the corresponding indexs of "delete_index" list'''
    '''data structure is the original list'''
    delete_index = sorted(delete_index)
    number_values_removed = 0
    for i in delete_index:
        del data_structure[i - number_values_removed]
        number_values_removed += 1

def keep_value_by_index_in_list(data_structure,store_index):
    ''' Create a new data structure that will only contain elements whose indexes can be found at store_index'''
    data_structure_temp = []
    for index in store_index:
        data_structure_temp.append(data_structure[index])
    return data_structure_temp

def delete_element_with_specific_value(data_structure_as_list,specific_value):
    delete_index = [i for i in range(len(data_structure_as_list)) if data_structure_as_list[i]==specific_value]
    delete_values_by_index_from_list(data_structure_as_list,delete_index)

def normalization_by_min(data_structure):
    '''Normalize each value by the minimum element to get the ratio'''
    if len(data_structure)==0:
        return
    min_value = data_structure[0]
    length_list = len(data_structure)
    for i in range(1,length_list):
        if data_structure[i] == 0:
            continue
        if min_value > data_structure[i]:
            min_value = data_structure[i]
    if min_value==0:
        return
    for index in range(length_list):
        data_structure[index] /= min_value

def normalize_probability_by_keys(data_structure):
    ''' It will normalize the probability so that the summation of all values of data_structure will be added to 1
    The sent data structure is a dictionary'''
    __iterative_normalization_keys(data_structure)

def __iterative_normalization_keys(data_structure):
    for key in data_structure:
        if type(data_structure[key])==dict:
            __iterative_normalization_keys(data_structure[key])
        else:
            sum_prob = sum([data_structure[value_key] for value_key in data_structure])
            # print(sum_prob)
            if sum_prob == 0:
                # print('Sum is 0 : '%(data_structure))
                return
            if round(sum_prob,5) != 1.0:
                for value_key in data_structure:
                    data_structure[value_key] /= sum_prob
            break

def sort_dict_by_values(dict,value_index):
    return sorted(dict.items(), key=itemgetter(value_index+1))

def normalize_probability_by_max_or_min(data_structure, abs_value = True, by_max=True):
    max_value = __iterative_find_maximum(data_structure, abs_value, by_max)
    __iterative_division_of_all_elements(data_structure,max_value)

def find_max_or_min_of_dictionary(data_structure,max_flag=True):
    return  __iterative_find_maximum(data_structure,False,max_flag)

def __iterative_find_maximum(data_structure, abs_value, by_max):
    index = 0
    maxx = -1
    for key in data_structure:
        if type(data_structure[key])==dict:
            current_max = __iterative_find_maximum(data_structure[key], abs_value, by_max)
            if by_max:
                if index==0 or maxx < current_max:
                    maxx = current_max
                index += 1
            else:
                if index==0 or maxx > current_max:
                    maxx = current_max
                index += 1
        else:
            if abs_value and by_max:
                maxx = max([abs(data_structure[value_key]) for value_key in data_structure])
            elif abs_value:
                minn = min([abs(data_structure[value_key]) for value_key in data_structure])
            elif not by_max:
                minn = min([data_structure[value_key] for value_key in data_structure])
            else:
                maxx = max([data_structure[value_key] for value_key in data_structure])
            return maxx
    return maxx

def __iterative_division_of_all_elements(data_structure,divider):
    for key in data_structure:
        if type(data_structure[key])==dict:
            __iterative_division_of_all_elements(data_structure[key],divider)
        else:
            for keys in data_structure:
                data_structure[keys] /= divider
            break