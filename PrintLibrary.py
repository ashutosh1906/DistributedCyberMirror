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

def state_space_print(state_space,print_parent=False):
    print('************************** State Space ***************************************')
    for state in state_space:
        state.print_properties(print_parent)

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

def possible_combinations_print(possible_combination,tag):
    print('***** Possible Combinations for %s ********'%(tag))
    for each_combination in possible_combination:
        print(each_combination)
    print('***** End of Possible Combinations for %s ********' % (tag))

def check_the_probability_transition(adversary_print = True):
    import POMDPSettings
    print('********* Probability Transition with Adversary *****************')
    for old_state_id in POMDPSettings.state_transition_with_adversary:
        old_state = POMDPSettings.state_space[old_state_id]
        print('Old State %s : %s'%(old_state.primary_key,old_state.adversary_positions))
        for new_state_id in POMDPSettings.state_transition_with_adversary[old_state_id]:
            new_state = POMDPSettings.state_space[new_state_id]
            print('\t Old %s to New State %s : %s' % (old_state_id,new_state.primary_key, new_state.adversary_positions))
            for node_actions in POMDPSettings.action_space_objects:
                for defense_action in node_actions:
                    print('\t\t Defense Action %s on Node %s'%(defense_action.primary_key,defense_action.node_id))
                    for adversary_action_id in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action.primary_key]:
                        adversary_action = POMDPSettings.adversary_action_objects[adversary_action_id]
                        if adversary_print:
                            print('\t\t\t Adversary Action %s : (Scan :: %s, Forward :: %s)' %
                                  (adversary_action.primary_key, adversary_action.perform_scan,adversary_action.forward))
                        print('\t\t\t Probability %s'%(POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action.primary_key][adversary_action_id]))
    print('********* End of Probability Transition with Adversary *****************')

def pomdp_expected_probability_transition():
    import POMDPSettings
    print('********* Expected Defender Probability Transition for POMDP *****************')
    for defense_action_id in POMDPSettings.state_transition_pomdp:
        did = POMDPSettings.defense_action_id_to_position[defense_action_id][0]
        dposition = POMDPSettings.defense_action_id_to_position[defense_action_id][1]
        defense_action = POMDPSettings.action_space_objects[did][dposition]
        for old_state_id in POMDPSettings.state_transition_pomdp[defense_action_id]:
            old_state = POMDPSettings.state_space[old_state_id]
            for new_state_id in POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id]:
                new_state = POMDPSettings.state_space[new_state_id]
                print('From %s:%s (V = %s) '%(old_state_id,old_state.adversary_positions,old_state.state_value),end='')
                print('To %s:%s (V = %s) ' % (new_state_id, new_state.adversary_positions,new_state.state_value), end='')
                print('Action %s:%s '%(defense_action_id,defense_action.node_id),end='')
                print('Probability %s'%(POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id][new_state_id]))

    print('********* End Expected Defender Probability Transition for POMDP *****************')

def probability_forward_from_old_to_new():
    import POMDPSettings
    print('********* Probability of Forwarding from one state to another *****************')
    for old_state_id in POMDPSettings.adversary_state_to_state_probability:
        old_state = POMDPSettings.state_space[old_state_id]
        for new_state_id in POMDPSettings.adversary_state_to_state_probability[old_state_id]:
            new_state = POMDPSettings.state_space[new_state_id]
            print('\t From State : %s to State : %s with Prob : %s'%(old_state.adversary_positions,new_state.adversary_positions,
                                                                     POMDPSettings.adversary_state_to_state_probability[old_state_id][new_state_id]))

    print('********* End of Probability of Forwarding from one state to another *****************')

def check_invalid_state_transition():
    print("\n ****** Invalid Transition Probability ************")
    import POMDPSettings
    for defense_id in POMDPSettings.state_transition_pomdp:
        dnode = POMDPSettings.defense_action_id_to_position[defense_id][0]
        dindex = POMDPSettings.defense_action_id_to_position[defense_id][1]
        defense = POMDPSettings.action_space_objects[dnode][dindex]
        for old_state_id in POMDPSettings.state_transition_pomdp[defense_id]:
            old_state = POMDPSettings.state_space[old_state_id]
            sum_prob = 0.0
            for new_state_id in POMDPSettings.state_transition_pomdp[defense_id][old_state_id]:
                new_state = POMDPSettings.state_space[new_state_id]
                sum_prob += POMDPSettings.state_transition_pomdp[defense_id][old_state_id][new_state_id]
            if round(sum_prob,3) != 1:
                print(" Error in %s:%s Value %s"%(old_state_id,old_state.adversary_positions,sum_prob))
    print(" ****** End of Invalid Transition Probability ************")

def observation_matrix():
    print("**** Printing Observation Matrix ******")
    import POMDPSettings
    for action in POMDPSettings.observation_probability:
        if action==POMDPSettings.WILDCARD_SYMBOL:
            print(" ***** Observation is Action Irrespective ****************")
        else:
            print("***** Defense Action : %s"%(action))
        for old_state_id in POMDPSettings.observation_probability[action]:
            old_state = POMDPSettings.state_space[old_state_id]
            print('***\t True State: %s --> %s'%(old_state_id,old_state.adversary_positions))
            sum_prob = 0.0
            for new_state_id in POMDPSettings.observation_probability[action][old_state_id]:
                new_state = POMDPSettings.state_space[new_state_id]
                print('***\t Observed State: %s --> %s with Prob : %s' % (new_state_id,
                                                                          new_state.adversary_positions,
                                                                          POMDPSettings.observation_probability[action][old_state_id][new_state_id]))
                sum_prob += POMDPSettings.observation_probability[action][old_state_id][new_state_id]
            print(" \t \t (^_^) Sum of Probability %s"%(sum_prob))
    print("**** End Printing Observation Matrix ******")


def rewards():
    print(" ****************** Print Rewards ********************")
    import POMDPSettings
    for old_state_id in POMDPSettings.rewards_pomdp:
        old_state = POMDPSettings.state_space[old_state_id]
        print('***\t Start State: %s --> %s ' % (old_state_id, old_state.adversary_positions))
        for new_state_id in POMDPSettings.rewards_pomdp[old_state_id]:
            new_state = POMDPSettings.state_space[new_state_id]
            print('End State: %s --> %s' % (new_state_id,new_state.adversary_positions),end='')
            for action_id in POMDPSettings.rewards_pomdp[old_state_id][new_state_id]:
                print('Defense Action: %s ' % (action_id),end='')
                if not POMDPSettings.PENALTY_WRONG_OBSERVATION:
                    print('Observations %s --> Values %s'%
                          (POMDPSettings.WILDCARD_SYMBOL,POMDPSettings.rewards_pomdp[old_state_id][new_state_id][action_id][POMDPSettings.WILDCARD_SYMBOL]))
    print(" ****************** End Printing Rewards ********************")

def defense_planning(time_sequence,defense_plan):
    print('\n At the end of time %s, Defense planning looks like this '%(time_sequence))
    import POMDPSettings
    for node in defense_plan:
        print('\t Node ID : %s'%(node))
        for defense_type in defense_plan[node]:
            if defense_type== POMDPSettings.SPATIAL_MUTATION_INDEX:
                print('\t\t Spatial Mutation %s'%(defense_plan[node][defense_type]))
            if defense_type== POMDPSettings.TEMPORAL_MUTATION_INDEX:
                print('\t\t Temporal Mutation %s'%(defense_plan[node][defense_type]))
            if defense_type== POMDPSettings.DIVERSITY_INDEX:
                print('\t\t Diversity %s'%(defense_plan[node][defense_type]))
            if defense_type== POMDPSettings.ANONYMIZATION_INDEX:
                print('\t\t Anonymization %s'%(defense_plan[node][defense_type]))
    print('******** Finished Planning *************')

def adversary_position_progression_by_time(adv_position):
    for i in range(len(adv_position)):
        print('Time Sequence --> %s'%(i))
        for pos in adv_position[i]:
            print('\t Position: %s Prob: %s Asset Value: %s'%(pos[0],pos[1],pos[2]))

def POMDP_dynamic_parameters(time_seq):
    import POMDPSettings
    print('Dynamic Parameters for time %s'%(time_seq))
    print('\t Regret Parameter %s'%(POMDPSettings.REGRET_PERCENTAGE))
    print('\t Cluster Difference %s'%(POMDPSettings.CLUSTER_DIFFERENCE))
    print('\t Min Effectiveness with Scan %s'%(POMDPSettings.MINIMUM_EFFECTIVENESS_WITH_SCAN))
    print('\t Min Effectiveness without Scan %s'%(POMDPSettings.MINIMUM_EFFECTIVENESS_WITHOUT_SCAN))
    print('\t Available Budget %s'%(POMDPSettings.MAXIMUM_BUDGET))


