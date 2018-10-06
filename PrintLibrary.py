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

def action_space_type_Print(action_space_by_type,action_space_group_index):
    print('*************************** Action Space by Type *****************************')
    print('\t%s'%(action_space_by_type))
    import POMDPSettings
    for action_group in action_space_group_index:
        if action_space_group_index[action_group]==POMDPSettings.SPATIAL_MUTATION_INDEX:
            print('************* Spatial Mutation Index %s ************'%(action_group))
        if action_space_group_index[action_group]==POMDPSettings.TEMPORAL_MUTATION_INDEX:
            print('************* Temporal Mutation Index %s ************'%(action_group))
        if action_space_group_index[action_group]==POMDPSettings.DIVERSITY_INDEX:
            print('************* Diversity Index %s ************'%(action_group))
        if action_space_group_index[action_group]==POMDPSettings.ANONYMIZATION_INDEX:
            print('************* Anonymization Index %s ************'%(action_group))

def action_space_Print(all_possible_action_space,possible_compromised_nodes,next_adversary_nodes,print_each_action):
    print('****** Printing Possible Action Space of numbers %s ******************'%(len(all_possible_action_space)))
    if print_each_action:
        for action in all_possible_action_space:
            print('\t %s'%(action))
    print("\t **** Currently Compromised nodes %s"%(possible_compromised_nodes))
    print("\t **** This action space is applicable to these nodes %s" % (next_adversary_nodes))
    print('****** End of Printing Possible Action Space of numbers ******************')

def comprehensive_action_space_print(action_space_objects):
    print("*********** Actions Space by Objects ***********************")
    for index in range(len(action_space_objects)):
        print('Node Index %s : Length is %s'%(index,len(action_space_objects[index])))
        for action in action_space_objects[index]:
            action.printProperties()
    print("*********** End Printing Actions Space by Objects ***********************")

def number_action_available_each_node(action_space_objects):
    for index in range(len(action_space_objects)):
        print("\t Node Type %s"%(index))
        print('\t Number of Actions %s'%(len(action_space_objects[index])))

def comprehensive_adversary_action_space(adversary_action_object):
    print('***************** Adversary Action Space ***********************')
    for action in adversary_action_object:
        action.printProperties()
    print('***************** End of Adversary Action Space ***********************')

def generic_information():
    import POMDPSettings
    print('Number of States %s'%(len(POMDPSettings.state_space)))
    number_defense_action = sum([len(i) for i in POMDPSettings.action_space_objects])
    print('Defender Action Space %s'%(number_defense_action))
    print('Defense Action To Map %s'%(POMDPSettings.defense_action_id_to_position))
    print('Adversary Action Space %s'%(len(POMDPSettings.adversary_action_objects)))
    print('Adversary Action Map %s'%(POMDPSettings.adversary_action_id_to_position))

