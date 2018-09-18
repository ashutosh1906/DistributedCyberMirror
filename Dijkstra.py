import heapq

def Dijkstra_algorithm_unweighted(source, adjacent_matrix):
    '''Find the shortest path to all nodes from the source node
    Return the output structured as dictionary where the keys are ids of the nodes and
    the value is the shortest distance'''
    # print("Neighbour Node %s"%(adjacent_matrix[source]))
    all_reachable_shortest_nodes = {}
    reachable_nodes = {}
    explored_node = {}
    min_priority_queue = []
    for node_id in adjacent_matrix[source]:
        if node_id not in reachable_nodes:
            reachable_nodes[node_id] = [1,node_id]
            heapq.heappush(min_priority_queue,reachable_nodes[node_id])

    ############################################### Dijkstra Starts from here #######################################
    explored_node[source] = 1
    while(len(min_priority_queue)>0):
        current_node = heapq.heappop(min_priority_queue)
        node_id = current_node[1]
        node_value = current_node[0]
        explored_node[node_id] = 1
        all_reachable_shortest_nodes[node_id] = node_value
        # print("Current Node :%s Edge %s Neighbour %s" % (node_id, node_value, adjacent_matrix[node_id]))
        try:
            for adjacent_node in adjacent_matrix[node_id]:
                if adjacent_node in explored_node:
                    continue
                if adjacent_node not in reachable_nodes:
                    reachable_nodes[adjacent_node] = [node_value+1,adjacent_node]
                    heapq.heappush(min_priority_queue,reachable_nodes[adjacent_node])
                else:
                    if node_value+1 < reachable_nodes[adjacent_node][0]:
                        reachable_nodes[adjacent_node][0] = node_value+1
                        heapq.heapify(min_priority_queue)
        except:
            print("Error ---> Current Node :%s Edge %s" % (node_id, node_value))

    print("Dijkstra's Output for Source: %s --> %s"%(source,all_reachable_shortest_nodes))

def Dijkstra_algorithm_unweighted_pair(source,target,adjacent_matrix,max_distance = 100000):
    '''Find the shortest distance between a source and a destination'''
    '''Maximum distance is treated as the optiional argument which if given as the parameter, will ignore any
    path with length greater than the max_distance'''
    all_reachable_shortest_nodes = {}
    reachable_nodes = {}
    explored_node = {}
    min_priority_queue = []
    pair_distance = -1
    if source==target:
        return 0 #################################### Source and target is same, soo length=0
    for node_id in adjacent_matrix[source]:
        if node_id==target:
            return 1 ############ target is the neighbour of source
        if node_id not in reachable_nodes:
            reachable_nodes[node_id] = [1, node_id]
            heapq.heappush(min_priority_queue, reachable_nodes[node_id])

    ############################################### Dijkstra Starts from here #######################################
    explored_node[source] = 1
    while (len(min_priority_queue) > 0):
        current_node = heapq.heappop(min_priority_queue)
        node_id = current_node[1]
        node_value = current_node[0]
        if node_value == max_distance:
            return -1 ################### No path between source and destination is short than the max distance
        explored_node[node_id] = 1
        all_reachable_shortest_nodes[node_id] = node_value
        # print("Current Node :%s Edge %s Neighbour %s" % (node_id, node_value, adjacent_matrix[node_id]))
        try:
            for adjacent_node in adjacent_matrix[node_id]:
                if adjacent_node==target:
                    pair_distance = node_value+1 ############################ Got the target
                    return pair_distance
                if adjacent_node in explored_node:
                    continue
                if adjacent_node not in reachable_nodes:
                    reachable_nodes[adjacent_node] = [node_value + 1, adjacent_node]
                    heapq.heappush(min_priority_queue, reachable_nodes[adjacent_node])
                else:
                    if node_value + 1 < reachable_nodes[adjacent_node][0]:
                        reachable_nodes[adjacent_node][0] = node_value + 1
                        heapq.heapify(min_priority_queue)
        except:
            print("Error ---> Current Node :%s Edge %s" % (node_id, node_value))

    return -1

