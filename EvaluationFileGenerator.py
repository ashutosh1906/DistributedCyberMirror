import random
directory = 'ConfigurationFiles/Adversary_files'
# path = [[689, 622, 556, 497, 6, 3], [995, 991, 911, 497, 6, 3]]
# path = [[723, 453, 8, 3],[979, 972, 336, 3]]
path = [[979, 972, 336, 3],[991, 911, 497, 6, 3]]
adj_matrix = {}
comp_prob = 1.0
target = 3
num_file = 0

def create_files(current_path,sort_desc = False):
    if sort_desc:
        current_path = sorted(current_path)
    global num_file
    num_file += 1
    file_pointer = open('%s/adv_position_%s_2'%(directory,num_file),'w')
    for position_index in range(len(current_path)-1):
        for node in current_path[position_index]:
            line = '%s,%s,%s'%(node,comp_prob,random.randint(1,10000))
            file_pointer.write('%s\n'%(line))
        file_pointer.write('-1\n')
    file_pointer.close()

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

if __name__=='__main__':
    initial_position = [target]
    # create_adj_matrix()
    create_adj_matrix_desc()
    print(adj_matrix)
    # dfs_traversal(initial_position,[])
    dfs_traversal_desc(sorted([path[0][0],path[1][0]]),[])

