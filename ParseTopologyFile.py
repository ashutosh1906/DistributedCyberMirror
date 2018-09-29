import re ##### For regular expression
import ast ######## The ast module helps Python applications to process trees of the Python abstract syntax grammar #############

def parse_aSHIIP_topology_with_size(topology_file_name, adjacent_matrix):
    '''Parse aSHIIP topology ::: arg1: Name of the topology file, arg2: adjacent_matrix'''
    topology_pointer = open(topology_file_name,'r+')
    size_found = False
    #################### Parser symbols ##############################
    number_of_node_symbol = 'Size :'

    for line in topology_pointer:
        line = line.replace('\n','')
        if not size_found:
            if number_of_node_symbol in line:
                number_of_node = int(line.replace(' ','').split(':')[1])
                del adjacent_matrix[:]
                for i in range(number_of_node):
                    adjacent_matrix.append([])
                print("Size of Topology : %s"%(len(adjacent_matrix)))
                size_found = True
        else:
            start_with_digit = re.match('^\d',line) ##################### Check if the string starts with a digit #####################################
            if start_with_digit is not None:
                line = line.replace(' ','')
                node_id = int(line[0:line.index('(')])
                adjacent_nodes = ast.literal_eval(line[line.index(')')+1:])
                for node_index in range(len(adjacent_nodes)):
                    adjacent_nodes[node_index] -= 1
                adjacent_matrix[node_id-1] = adjacent_nodes

def parse_aSHIIP_topology(topology_file_name, adjacent_matrix):
    '''Parse aSHIIP topology ::: arg1: Name of the topology file, arg2: adjacent_matrix'''
    topology_pointer = open(topology_file_name, 'r+')
    del adjacent_matrix[:]
    for line in topology_pointer:
        line = line.replace('\n', '')
        start_with_digit = re.match('^\d',line)  ##################### Check if the string starts with a digit #####################################
        if start_with_digit is not None:
            line = line.replace(' ', '')
            node_id = int(line[0:line.index('(')])
            adjacent_nodes = ast.literal_eval(line[line.index(')') + 1:])
            for node_index in range(len(adjacent_nodes)):
                adjacent_nodes[node_index] -= 1
            adjacent_matrix.append(adjacent_nodes)
    topology_pointer.close()

def parse_aSHIIP_topology_bi_directional(topology_file_name, adjacent_matrix):
    '''Parse aSHIIP topology ::: arg1: Name of the topology file, arg2: adjacent_matrix'''
    topology_pointer = open(topology_file_name, 'r+')
    del adjacent_matrix[:]
    for line in topology_pointer:
        line = line.replace('\n', '')
        start_with_digit = re.match('^\d',line)  ##################### Check if the string starts with a digit #####################################
        if start_with_digit is not None:
            line = line.replace(' ', '')
            node_id = int(line[0:line.index('(')])
            adjacent_nodes = ast.literal_eval(line[line.index(')') + 1:])
            for node_index in range(len(adjacent_nodes)):
                adjacent_nodes[node_index] -= 1
            adjacent_matrix.append(adjacent_nodes)
    topology_pointer.close()

    for node_id in range(len(adjacent_matrix)):
        for adj_node in adjacent_matrix[node_id]:
            if node_id not in adjacent_matrix[adj_node]:
                adjacent_matrix[adj_node].append(node_id)