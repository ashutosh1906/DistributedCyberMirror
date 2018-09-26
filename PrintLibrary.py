def shortest_path_print(source,paths):
    if source not in paths:
        print('No knowledge about the shortest path towards the source node : %s'%(source))
    else:
        print('Shortest path towards the source %s'%(source))
        print('\t The list %s'%(paths[source]))

def all_pair_shortest_path_print(paths):
    print('******************************* Printing all pairs shortest path************************************************')
    for source in paths:
        print('Shortest path towards the source %s' % (source))
        print('\t The list %s' % (paths[source]))
    print(
        '******************************* End of Printing all pairs shortest path************************************************')

def score_compromised_node(compromised_nodes):
    print(
        '******************************* Printing score of compromised nodes ************************************************')
    for node in compromised_nodes:
        print('Node ID: %s and Score: %s'%(node,compromised_nodes[node]))
    print(
        '******************************* End of Printing score of compromised nodes ************************************************')

def state_space_print(state_space):
    print('************************** State Space ***************************************')
    for state in state_space:
        state.print_properties()