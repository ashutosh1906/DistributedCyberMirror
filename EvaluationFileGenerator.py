import random
import sys
from CommonUtilities import DataStructureFunctions
directory = 'ConfigurationFiles/Adversary_files_test'
topology_dir = 'InputFiles/Topology'
# path = [[689, 622, 556, 497, 6, 3], [995, 991, 911, 497, 6, 3]]
# path = [[723, 453, 8, 3],[979, 972, 336, 3]]
# path = [[979, 972, 336, 3],[991, 911, 497, 6, 3]]
#path = [[723, 453, 8, 3],[979, 972, 336, 3],[984, 982, 972, 336, 3]]
#path = [[689, 622, 556, 497, 6, 3]]
path = None#[[7,5,3,1,0],[8,6,4,2,0]]
adj_matrix = {}
comp_prob = 1.0
target = 0
num_file = 0
path_exist = {}
files_created = 0
NUMBER_OF_NODES = 14
DEGREE = 3
DEPTH_BRANCH = 2


def create_files(current_path,sort_desc = False):
    if sort_desc:
        current_path = sorted(current_path)
    global num_file
    num_file += 1
    file_pointer = open('%s/adv_position_%s_%s_%s'%(directory,NUMBER_OF_NODES,DEGREE,num_file),'w')
    for position_index in range(len(current_path)-1):
        for node in current_path[position_index]:
            line = '%s,%s,%s'%(node,comp_prob,random.randint(1,10000))
            file_pointer.write('%s\n'%(line))
        file_pointer.write('-1\n')
    file_pointer.close()
    if num_file==3:
        sys.exit()

def dfs_traversal(current_position,current_path):
    # print('%s %s'%(current_position,current_path))
    current_position_path = []
    for node in current_position:
        current_position_path.append(node)

    current_path.append(sorted(current_position_path))
    if len(current_position)==len(path):
        all_last = True
        for node in current_position:
            if node in adj_matrix:
                all_last = False
                break

        if all_last:
            print('One Path %s'%(current_path))
            create_files(current_path)
            del current_path[-1]
            return


    # print('%s %s' % (current_position, current_path))
    for index in range(len(current_position)):
        current_node = current_position[index]
        if current_node not in adj_matrix:
            continue
        # print('Current Node %s --> %s' % (current_node, adj_matrix[current_node]))
        del current_position[index]
        for child in adj_matrix[current_node]:
            current_position.insert(0,child)
        dfs_traversal(current_position,current_path)
        for child in adj_matrix[current_node]:
            del current_position[0]
        current_position.insert(index,current_node)
    del current_path[-1]


def create_adj_matrix():
    for path_ind in path:
        for node_index in range(1,len(path_ind)):
            node = path_ind[node_index]
            if node not in adj_matrix:
                adj_matrix[node] = [path_ind[node_index-1]]
            else:
                if path_ind[node_index-1] not in adj_matrix[node]:
                    adj_matrix[node].append(path_ind[node_index-1])

def dfs_traversal_desc(current_position,current_path):
    # print('%s %s' % (current_position, current_path))
    current_position_path = []
    for node in current_position:
        current_position_path.append(node)
    current_path.append(sorted(current_position_path))
    for node in current_position:
        if node==target:
            print("Path %s"%(current_path))
            create_files(current_path)
            del current_path[-1]
            return
    # print('--> %s %s' % (current_position, current_path))
    if len(current_position)==2:
        if adj_matrix[current_position[0]] == adj_matrix[current_position[1]]:
            node = current_position[0]
            del current_position[:]
            current_position.append(adj_matrix[node][0])
            dfs_traversal_desc(current_position, current_path)
            del current_position[0]
            for node in current_position_path:
                current_position.append(node)
        else:
            # print('--> --> %s %s' % (current_position, current_path))
            for node_index in range(len(current_position)):
                node = current_position[node_index]
                next_node = adj_matrix[node][0]
                if next_node in path[0] and next_node in path[1]:
                    del current_position[:]
                    current_position.append(next_node)
                    dfs_traversal_desc(current_position, current_path)
                    del current_position[0]
                    for node in current_position_path:
                        current_position.append(node)
                else:
                    del current_position[node_index]
                    current_position.insert(node_index,adj_matrix[node][0])
                    dfs_traversal_desc(current_position, current_path)
                    del current_position[node_index]
                    current_position.insert(node_index,node)
    elif len(current_position)==1:
        node = current_position[0]
        del current_position[0]
        current_position.insert(0, adj_matrix[node][0])
        dfs_traversal_desc(current_position, current_path)
        del current_position[0]
        current_position.insert(0,node)

    del current_path[-1]



def create_adj_matrix_desc():
    for path_ind in path:
        for node_index in range(len(path_ind)-1):
            node = path_ind[node_index]
            if node not in adj_matrix:
                adj_matrix[node] = [path_ind[node_index+1]]
            else:
                if path_ind[node_index+1] not in adj_matrix[node]:
                    adj_matrix[node].append(path_ind[node_index+1])

def dfs_many_nodes(current_position,current_path):

    current_position_temp = []
    for node in current_position:
        current_position_temp.append(node)
    current_path.append(current_position_temp)
    # print('S --> P %s %s ' % (current_position, current_path))

    for node in current_position:
        if node==target:
            print("Path %s" % (current_path))
            create_files(current_path)
            del current_path[-1]
            return

    node_index = 0
    previously_explored = {}
    for node in current_position_temp:
        # print('Current Node %s'%(node))
        if adj_matrix[node][0] in previously_explored:
            continue
        path_index = 0
        for path_ind in path:
            if node in path_ind:
                next_node = adj_matrix[node][0]
                previously_explored[next_node] = 1
                other_node_index = 0
                other_node_delete = []
                for other_nodes in current_position:
                    if other_nodes==node:
                        other_node_index += 1
                        continue
                    for path_ind_other in path:
                        if other_nodes in path_ind_other:
                            if next_node in path_ind_other:
                                other_node_delete.append(other_node_index)
                                break
                    other_node_index += 1
                # print('%s %s'%(current_position,other_node_delete))
                del current_position[node_index]
                current_position.insert(node_index, next_node)
                DataStructureFunctions.delete_values_by_index_from_list(current_position,other_node_delete)

                dfs_many_nodes(sorted(current_position),current_path)
                del current_position[:]
                for past_node in current_position_temp:
                    current_position.append(past_node)
                break

            path_index += 1
        node_index += 1
    del current_path[-1]
    # print('End S --> P %s %s ' % (current_position, current_path))

def generate_topology(tree_depth,degree=1):
    number_of_nodes = tree_depth*degree
    line_file = [None for i in range(number_of_nodes)]
    file = open('%s/Topo_%s_%s'%(topology_dir,tree_depth,degree),'w')
    node_index = 0
    first_line = ''
    child_index = node_index+1
    for i in range(int(tree_depth*degree/2)):
        first_line = '%s (%s) [%s]'%(child_index,child_index,child_index+1)
        child_index += 1
        line_file[i] = first_line
    print(child_index)

    first_line = '%s (%s) [' % (child_index, child_index)
    for i in range(degree):
        first_line = '%s%s' % (first_line,child_index+i+1)
        if i!=(degree-1):
            first_line = '%s,' % (first_line)
    first_line = '%s]' % (first_line)
    # print(first_line)
    line_file[child_index-1] = first_line
    child_index += 1
    node_index = child_index
    print(node_index)

    left_over_depth = int((number_of_nodes-node_index+1)/2)
    print(left_over_depth)
    for i in range(degree):
        child_index = node_index+i

        for depth in range(left_over_depth):
            current_node_index = child_index+depth*degree
            first_line = '%s (%s) [%s]' % (current_node_index,current_node_index,child_index+(depth+1)*degree)
            print(first_line)
            line_file[current_node_index-1] = first_line
        current_node_index = child_index + (left_over_depth-1)* degree
        first_line = '%s (%s) []' % (current_node_index, current_node_index)
        print(first_line)
        line_file[current_node_index - 1] = first_line
    for i in range(number_of_nodes):
        file.write('%s\n' % (line_file[i]))
    file.close()

def generate_path(number_of_nodes,one_degree_node, degree=1):
    global path
    path = [[j for j in range(one_degree_node, -1, -1)] for i in range(degree)]
    for i in range(degree):
        path[i].insert(0, path[i][0] + i + 1)
    left_over_depth = int((number_of_nodes - path[0][0] + 1) / degree)
    # print('%s -- %s'%(path,left_over_depth))

    for path_index in range(degree):
        for i in range(left_over_depth-1):
            path[path_index].insert(0,path[path_index][0]+degree)
    print(path)


def geanerate_topology_3(number_of_nodes,degree_depth,degree):
    one_node_length = number_of_nodes-degree_depth*degree
    line_file = [None for i in range(number_of_nodes)]
    file = open('%s/Topo_%s_%s' % (topology_dir,number_of_nodes,degree), 'w')
    for i in range(one_node_length-1):
        first_line = '%s (%s) [%s]' % (i, i, i + 1)
        line_file[i] = first_line

    node_index = one_node_length-1
    first_line = '%s (%s) ['%(node_index,node_index)
    for i in range(degree-1):
        first_line = '%s%s,'%(first_line,node_index+i+1)
    first_line = '%s%s]' % (first_line,node_index+degree)
    line_file[node_index] = first_line

    for i in range(degree):
        for j in range(degree_depth):
            child_index = node_index + i + 1 + j*degree
            print(child_index)
            if j==degree_depth-1:
                first_line = '%s (%s) []' % (child_index, child_index)
            else:
                first_line = '%s (%s) [%s]' %(child_index,child_index,child_index+degree)
            line_file[child_index] = first_line

    for i in range(number_of_nodes):
        file.write('%s\n'%(line_file[i]))
    file.close()

def generate_adversary_files():
    generate_path(NUMBER_OF_NODES,NUMBER_OF_NODES-DEPTH_BRANCH*DEGREE-1,DEGREE)
    initial_position = [target]
    create_adj_matrix_desc()
    print(adj_matrix)
    current_position = []
    global path
    for path_ind in path:
        current_position.append(path_ind[0])
    dfs_many_nodes(sorted(current_position), [])
    print('Number of generated files %s' % (num_file))

if __name__=='__main__':
    generate_adversary_files()
    # geanerate_topology_3(18,3,3)



