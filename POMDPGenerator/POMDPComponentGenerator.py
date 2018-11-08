from Components import State,Actions
import POMDPSettings
from CommonUtilities import SetOperations
from CommonUtilities import DataStructureFunctions
import Utilities,PrintLibrary
import random,math
from CommonUtilities import GraphTraversal
import PrintLibrary

def generate_initial_state_space(possible_nodes_for_state):
    print('**** Possible Initial Adversary Positions %s'%(possible_nodes_for_state))
    compromised_hosts_by_position = list(possible_nodes_for_state.keys())
    taken_node = {}
    adv_position_node = []
    for i in range(len(compromised_hosts_by_position)):
        adv_position_node.append([])
        for node in possible_nodes_for_state[compromised_hosts_by_position[i]]:
            adv_position_node[i].append(node)
            # if node==compromised_hosts_by_position[i] or POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
            #     adv_position_node[i].append(-node)

    print("Adversary Position Nodes %s"%(adv_position_node))
    POMDPSettings.adversary_position_nodes = adv_position_node
    POMDPSettings.compromised_nodes_current_time = compromised_hosts_by_position

    # iterate_over_possible_state(adv_position_node,1,len(compromised_hosts_by_position),[])
    possible_node_combinations = GraphTraversal.graph_traversal_concurrent(POMDPSettings.adversary_position_nodes)
    # PrintLibrary.possible_combinations_print(possible_node_combinations, 'Nodes Positions')
    if POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
        POMDPSettings.possible_node_combinations = create_mirror_corresponding_nodes(possible_node_combinations)
    else:
        POMDPSettings.possible_node_combinations = []
        for comb in possible_node_combinations:
            POMDPSettings.possible_node_combinations.append(comb)
        length_adversary_positions = len(POMDPSettings.adversary_position_nodes)
        ################ If the adversary initialyy doesn't exist in one position ######################
        # for j in range(0,length_adversary_positions):
        #     for i in range(j,length_adversary_positions):
        #         possible_node_combinations = GraphTraversal.graph_traversal_concurrent(POMDPSettings.adversary_position_nodes[j:i+1])
        #         for comb in possible_node_combinations:
        #             POMDPSettings.possible_node_combinations.append(comb)
    # PrintLibrary.possible_combinations_print(POMDPSettings.possible_node_combinations, 'Nodes Positions')
    ######################### Generate States ####################################
    determine_parent_nodes()
    state_id = 0
    # del POMDPSettings.state_space[:]
    # POMDPSettings.state_space_map.clear()
    for adv_positions in POMDPSettings.possible_node_combinations:
        if POMDPSettings.SORT_ADVERSARY_POSITION:
            adv_positions = sorted(adv_positions)
        if tuple(adv_positions) not in POMDPSettings.state_space_map:
            POMDPSettings.state_space.append(State.State(state_id,adv_positions))
            POMDPSettings.state_space_map[tuple(adv_positions)] = state_id
            state_id += 1

def create_mirror_corresponding_nodes(possible_node_combinations):
    org_possible_node_combinations = []
    for positions in possible_node_combinations:
        if len(positions)==1:
            org_possible_node_combinations.append([positions[0]])
            org_possible_node_combinations.append([-positions[0]])
        if len(positions)>1:
            start_node = positions[0]
            iterate_over_mirror_nodes(positions[1:],[start_node],org_possible_node_combinations)
            iterate_over_mirror_nodes(positions[1:],[-start_node],org_possible_node_combinations)
    return org_possible_node_combinations

def iterate_over_mirror_nodes(data_structure,chosen_node,possible_node_combinations):
    if len(data_structure)==1:
        for i in range(2):
            current_state_position = []
            for node in chosen_node:
                current_state_position.append(node)
            current_state_position.append(data_structure[0]*pow(-1,i))
            possible_node_combinations.append(current_state_position)
    else:
        start_node = data_structure[0]
        for i in range(2):
            chosen_node.append(start_node*pow(-1,i))
            iterate_over_mirror_nodes(data_structure[1:],chosen_node,possible_node_combinations)
            del chosen_node[-1]

def determine_parent_nodes():
    POMDPSettings.parent_nodes_considered_paths.clear()
    # print('Possible Nodes for State %s'%(POMDPSettings.possible_nodes_for_state))
    for compromised_node in POMDPSettings.possible_nodes_for_state:
        node_index = 0
        for node in POMDPSettings.possible_nodes_for_state[compromised_node]:
            if node not in POMDPSettings.parent_nodes_considered_paths:
                POMDPSettings.parent_nodes_considered_paths[node] = []
            if node_index > 0:
                parent_node = POMDPSettings.possible_nodes_for_state[compromised_node][node_index-1]
                if parent_node not in POMDPSettings.parent_nodes_considered_paths[node]:
                    POMDPSettings.parent_nodes_considered_paths[node].append(parent_node)
            node_index += 1
    # print('Parent %s'%(POMDPSettings.parent_nodes_considered_paths))

def iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,current_depth,
                                 chosen_node,state_space,state_space_map):
    if current_depth > len(compromised_nodes_current_time):
        # print('*** Assign and Update Belief of the States %s :: %s'%(chosen_node,state_space_map[tuple(chosen_node)]))
        prob = 1.0
        for node in chosen_node:
            if node in compromised_nodes_probability:
                prob *= compromised_nodes_probability[node]
            if -node in compromised_nodes_probability:
                prob *= (1-compromised_nodes_probability[-node])
        if POMDPSettings.SORT_ADVERSARY_POSITION:
            state_id = state_space_map[tuple(sorted(chosen_node))]
        # print(
        #     '*** Assign and Update Belief of the States %s :: %s --> %s' % (chosen_node,state_id,prob))
        state_space[state_id].set_belief(prob)
        return
    first_adv_position = compromised_nodes_current_time[current_depth-1]
    chosen_node.append(first_adv_position)
    iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,
                                 current_depth+1,chosen_node,state_space,state_space_map)
    del chosen_node[-1]
    if POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
        chosen_node.append(-first_adv_position)
        iterate_over_possible_belief(compromised_nodes_current_time, compromised_nodes_probability,
                                    current_depth + 1,
                                    chosen_node,state_space,state_space_map)
        del chosen_node[-1]

def generate_initial_belief(compromised_nodes_current_time,compromised_nodes_probability,state_space,state_space_map):
    print('***** Selectected Compromised Nodes %s'%(compromised_nodes_current_time))
    print('***** Selectected Compromised Nodes Prob %s' % (compromised_nodes_probability))
    print('******* State Space ************** %s'%(len(state_space)))
    # print('******* State Space Map ************** %s' % (state_space_map))
    iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,
                                 1,[],state_space,state_space_map)

def initialize_action_space():
    index = 0
    if POMDPSettings.SPATIAL_MUTATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.SPATIAL_MUTATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.spatial_mutation)
        index += 1

    if POMDPSettings.TEMPORAL_MUTATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.TEMPORAL_MUTATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.temporal_mutation)
        index += 1

    if POMDPSettings.DIVERSITY_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.DIVERSITY_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.diversity)
        index += 1

    if POMDPSettings.ANONYMIZATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.ANONYMIZATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.anonymization)
        index += 1

    POMDPSettings.action_space_all_values = \
        SetOperations.combination_possible_values_all_positions(POMDPSettings.action_space_by_type)

def generate_action_space():
    id = 0
    node_id = 0
    # print('Next Adversary Nodes %s'%(POMDPSettings.next_adversary_nodes))
    for node in POMDPSettings.next_adversary_nodes:
        # print('Check Node %s'%(node))
        POMDPSettings.action_space_objects.append([])
        for action_value in POMDPSettings.action_space_all_values:
            if any([True for sp_action in action_value if sp_action!=1]):
                POMDPSettings.action_space_objects[node_id].append(Actions.Actions(id,node,action_value))
                id += 1
        node_id += 1

    POMDPSettings.DEFENSE_ACTION_TOTAL = id
    ############################ Determine the co-efficients (Uniform) ############################
    __determine_co_efficients_uniform()
    # print(' Weights: %s, %s, %s' % (POMDPSettings.WEIGHT_CONCEALABILITY_MEASURE,POMDPSettings.WEIGHT_DETECTABILITY_MEASURE,
    #                                 POMDPSettings.WEIGHT_DETERRENCE_MEASURE))
    set_effectiveness_over_all_actions(POMDPSettings.action_space_objects)

def set_effectiveness_over_all_actions(action_space_objects):
    for index in range(len(action_space_objects)):
        for action in action_space_objects[index]:
            action.set_effectiveness()

def __determine_co_efficients_uniform():
    num_parameters = 0
    if POMDPSettings.CONCEALABILITY_MEASURE_ENABLED:
        num_parameters += 1
    if POMDPSettings.DETECTABILITY_MEASURE:
        num_parameters += 1
    if POMDPSettings.DETERRENCE_MEASURE:
        num_parameters += 1
    POMDPSettings.WEIGHT_CONCEALABILITY_MEASURE = POMDPSettings.WEIGHT_DETECTABILITY_MEASURE = POMDPSettings.WEIGHT_DETERRENCE_MEASURE = 1/num_parameters

def set_weighted_cost_effectiveness_action_space():
    for action_type in POMDPSettings.action_space_objects:
        for action in action_type:
            weighted_effectiveness_action = 0.0
            weighted_effectiveness_action += POMDPSettings.ADVERSARY_SCANNING_PROB * action.effeciveness_with_scan
            weighted_effectiveness_action += (1 - POMDPSettings.ADVERSARY_SCANNING_PROB) * action.effeciveness_without_scan
            action.set_weighted_effectiveness(weighted_effectiveness_action)
            if action.cost==0:
                action.set_weighted_cost_effectiveness(0.0)
            else:
                weighted_cost_effectiveness_action = weighted_effectiveness_action*100/action.cost
                action.set_weighted_cost_effectiveness(weighted_cost_effectiveness_action)

def marginal_prunning(action_space_objects):
    # print("***** Before Marginal Prunning Number of Actions ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)
    for node_index in range(len(action_space_objects)):
        list_of_remove = []
        for index in range(len(action_space_objects[node_index])):
            action = action_space_objects[node_index][index]
            # action.printProperties()
            if action.effeciveness_with_scan < POMDPSettings.MINIMUM_EFFECTIVENESS_WITH_SCAN:
                list_of_remove.append(index)
                # print("Pruned Out : Action Effectiveness with Scan %s ID %s"%(action.effeciveness_with_scan,action.primary_key))
                continue
            if action.effeciveness_without_scan < POMDPSettings.MINIMUM_EFFECTIVENESS_WITHOUT_SCAN:
                list_of_remove.append(index)
                # print("Pruned Out : Action Effectiveness without Scan %s ID %s" % (action.effeciveness_without_scan,action.primary_key))
                continue
        DataStructureFunctions.delete_values_by_index_from_list(POMDPSettings.action_space_objects[node_index],list_of_remove)
    # print("***** After Marginal Prunning Number of Actions ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)

def redundant_prunning(action_space_objects):
    # print("****** Before Redundant Prunning %s******"%(len(action_space_objects)))
    weighted_effectiveness_action = [] ###### Index of a value in this list is also representing the index in the action space
    weighted_cost_effectiveness_action = []
    effectiveness_action_scan = []
    effectiveness_action_without_scan = []
    for action in action_space_objects:
        weighted_effectiveness_action.append(action.weighted_effectiveness)
        effectiveness_action_scan.append(action.effeciveness_with_scan)
        effectiveness_action_without_scan.append(action.effeciveness_without_scan)
        if POMDPSettings.Y_AXIS_COST_EFFECTIVENESS:
            weighted_cost_effectiveness_action.append(action.weighted_cost_effectiveness)
        else:
            weighted_cost_effectiveness_action.append(action.cost)
    # print(weighted_effectiveness_action)
    # print(weighted_cost_effectiveness_action)
    number_of_cluster = (max(weighted_effectiveness_action)-min(weighted_effectiveness_action))/POMDPSettings.CLUSTER_DIFFERENCE
    if number_of_cluster != int(number_of_cluster):
        number_of_cluster = int(number_of_cluster)+1

    min_cluster = number_of_cluster
    max_cluster = min_cluster + POMDPSettings.MAX_CLUSTER_ITERATION + 1
    best_selection = None
    best_selection_distance = None
    best_cluster_size = None
    for cluster_size in range(min_cluster,max_cluster):
        if POMDPSettings.THREE_DIMENSIONAL_CLUSTER:
            selected_action, distance = Utilities.create_clusters_three_dimensional(effectiveness_action_scan,effectiveness_action_without_scan,
                                                                                    weighted_cost_effectiveness_action,
                                                                                    weighted_effectiveness_action,cluster_size)
        else:
            selected_action,distance = Utilities.create_clusters(weighted_effectiveness_action,weighted_cost_effectiveness_action,cluster_size)
        if best_selection is None \
                or best_selection_distance > distance:
            best_selection = selected_action
            best_selection_distance = distance
            best_cluster_size = cluster_size

    # print('Cluster Size %s\n\tSelected Action : %s with distance %s'%(best_cluster_size,best_selection,best_selection_distance))

    action_space_objects = DataStructureFunctions.keep_value_by_index_in_list(action_space_objects,best_selection)
    # print("****** After Redundant Prunning %s******" % (len(action_space_objects)))
    return action_space_objects

def irrelevant_prunning(action_space_objects):
    # print("****** Before Irrelevant Prunning ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)
    for node_index in range(len(action_space_objects)):
        dict_cost_vs_effectiveness = {}
        index = 0
        for action in action_space_objects[node_index]:
            dict_cost_vs_effectiveness[index] = [action.cost,action.weighted_effectiveness]
            index += 1
        # print("Irrelevant Prunning %s"%(dict_cost_vs_effectiveness))
        sorted_list = DataStructureFunctions.sort_dict_by_values(dict_cost_vs_effectiveness,0)
        # print(sorted_list)
        seen_effectiveness = []
        delete_element = []
        for action_property in sorted_list:
            if len(seen_effectiveness) == 0:
                seen_effectiveness.append(action_property[1][1])
                continue
            else:
                current_id = action_property[0]
                current_effectiveness = action_property[1][1]
                if current_effectiveness <= seen_effectiveness[-1]:
                    delete_element.append(current_id)
                else:
                    seen_effectiveness.append(current_effectiveness)
        # print(seen_effectiveness)
        # print('Delete %s'%(delete_element))
        DataStructureFunctions.delete_values_by_index_from_list(action_space_objects[node_index],delete_element)

    # print("****** After Irrelevant Prunning ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)

################################################# Related to State Transition ##################################################
def state_transition_initializations():
    ######## Previous State (key)---> Next State (Value) ###########################
    non_zero_transition = 0
    for new_state in POMDPSettings.state_space:
        new_state_id = POMDPSettings.state_space_map[tuple(new_state.adversary_positions)]
        for old_state_id in new_state.parent_states:
            if old_state_id not in POMDPSettings.state_transition_with_adversary:
                POMDPSettings.state_transition_with_adversary[old_state_id]={new_state_id:{}}
            elif new_state_id not in POMDPSettings.state_transition_with_adversary[old_state_id]:
                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id] = {}

    ########################### Add the state transition when the state is not changed #########################
    for new_state in POMDPSettings.state_space:
        new_state_id = POMDPSettings.state_space_map[tuple(new_state.adversary_positions)]
        if new_state_id not in POMDPSettings.state_transition_with_adversary:
            POMDPSettings.state_transition_with_adversary[new_state_id] = {}
        POMDPSettings.state_transition_with_adversary[new_state_id][new_state_id] = {}

    # print('*************** Non Zero Transitions %s*****************'%(non_zero_transition))
    # print('*************** State Transitions %s*****************' % (POMDPSettings.state_transition_with_adversary))
    adversary_probability_update()

    ###################################### Initialize the probability for state transition ######################################
    for old_state_id in POMDPSettings.state_transition_with_adversary:
        for new_state_id in POMDPSettings.state_transition_with_adversary[old_state_id]:
            for node_actions in POMDPSettings.action_space_objects:
                for defense_action in node_actions:
                    POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action.primary_key] = {}
                    for adversary_action in POMDPSettings.adversary_action_objects:
                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action.primary_key][adversary_action.primary_key] = 0.0

def assign_state_transition_probability_with_adversary():
    for old_state_id in POMDPSettings.state_transition_with_adversary:
        old_state = POMDPSettings.state_space[old_state_id]
        for new_state_id in POMDPSettings.state_transition_with_adversary[old_state_id]:
            new_state = POMDPSettings.state_space[new_state_id]
            for defense_action_id in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id]:
                defense_action_node_roll = POMDPSettings.defense_action_id_to_position[defense_action_id][0]
                defense_action_position = POMDPSettings.defense_action_id_to_position[defense_action_id][1]
                defense_action = POMDPSettings.action_space_objects[defense_action_node_roll][defense_action_position]
                if (defense_action_id != defense_action.primary_key) or False:
                    print('New State %s Old State %s Defense Action %s==%s' %
                          (new_state.adversary_positions,old_state.adversary_positions,defense_action_id,defense_action.primary_key))
                for adversary_action_id in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id]:
                    adversary_action = POMDPSettings.adversary_action_objects[adversary_action_id]

                    #################### All possible positions are mirrors or the adversary already reached target ################################
                    if len(old_state.adversary_positions)==old_state.number_mirror_node or old_state.adversary_positions==POMDPSettings.target_node:
                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id][
                            adversary_action_id] = 1.0
                        continue
                    ########################################### If the adversary forwards #############################################
                    if not adversary_action.forward:
                        if old_state.adversary_positions == new_state.adversary_positions:
                            POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id][adversary_action_id] = 1.0
                        else:
                            POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                defense_action_id][adversary_action_id] = 0.0

                    ########################################### If the adversary does not forward ##########################
                    elif adversary_action.forward:
                        if old_state.adversary_positions == new_state.adversary_positions:
                            if adversary_action_id not in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id]:
                                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                    defense_action_id][adversary_action_id] = 0.0
                            continue

                        defense_node = defense_action.node_id
                        forward_probability = POMDPSettings.adversary_state_to_state_probability[old_state_id][new_state_id]
                        # print("F %s"%(forward_probability))
                        ####################################### If the adversary scans ##########################
                        if adversary_action.perform_scan:
                            if defense_node in new_state.adversary_positions:
                                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                    defense_action_id][adversary_action_id] = (1-defense_action.effeciveness_with_scan)*forward_probability
                                if not POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
                                    if adversary_action_id not in \
                                            POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                                defense_action_id]:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = 0.0
                                    POMDPSettings.state_transition_with_adversary[old_state_id][old_state_id][
                                        defense_action_id][adversary_action_id] += 1-\
                                                                                  POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id][adversary_action_id]
                            elif -defense_node in new_state.adversary_positions:
                                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                    defense_action_id][adversary_action_id] = defense_action.effeciveness_with_scan*forward_probability
                            else:
                                # if old_state.number_mirror_node == new_state.number_mirror_node:
                                #     POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                #         defense_action_id][adversary_action_id] = forward_probability
                                if old_state.number_mirror_node >= new_state.number_mirror_node:
                                    unexpected_mirror_exist = False
                                    for mirror_node in new_state.adversary_positions:
                                        if mirror_node >= 0:
                                            continue
                                        if mirror_node not in old_state.adversary_positions:
                                            unexpected_mirror_exist = True
                                    if unexpected_mirror_exist:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = 0
                                    else:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = forward_probability
                                else:
                                    POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                        defense_action_id][adversary_action_id] = 0
                        ##################################### If the adversary does not scan #####################
                        else:
                            if defense_node in new_state.adversary_positions:
                                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                    defense_action_id][adversary_action_id] = (1-defense_action.effeciveness_without_scan)*forward_probability
                                if not POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
                                    if adversary_action_id not in \
                                            POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                                defense_action_id]:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = 0.0
                                    POMDPSettings.state_transition_with_adversary[old_state_id][old_state_id][
                                        defense_action_id][adversary_action_id] += 1-\
                                                                                  POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id][adversary_action_id]
                            elif -defense_node in new_state.adversary_positions:
                                POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                    defense_action_id][adversary_action_id] = defense_action.effeciveness_without_scan*forward_probability
                            else:
                                # if old_state.number_mirror_node == new_state.number_mirror_node:
                                #     POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                #         defense_action_id][adversary_action_id] = forward_probability
                                if old_state.number_mirror_node >= new_state.number_mirror_node:
                                    unexpected_mirror_exist = False
                                    for mirror_node in new_state.adversary_positions:
                                        if mirror_node >= 0:
                                            continue
                                        if mirror_node not in old_state.adversary_positions:
                                            unexpected_mirror_exist = True
                                    if unexpected_mirror_exist:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = 0
                                    else:
                                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                            defense_action_id][adversary_action_id] = forward_probability
                                else:
                                    POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][
                                        defense_action_id][adversary_action_id] = 0

def update_state_value_from_leaves():
    '''Update the state value based on the (Parent,Child) of the tree'''
    POMDPSettings.node_values.clear()
    print('*** Parent Nodes %s ****'%(POMDPSettings.parent_nodes_considered_paths))
    for node in POMDPSettings.parent_nodes_considered_paths:
        this_value = 0
        for child in POMDPSettings.parent_nodes_considered_paths[node]:
            if child in POMDPSettings.node_values:
                this_value += POMDPSettings.node_values[child]
            else:
                this_value += recursive_child_value_upated(child,POMDPSettings.node_values)
        target = POMDPSettings.target_node[0]
        distance_from_target = POMDPSettings.all_pair_shortest_path[target][node]
        POMDPSettings.node_values[node] = this_value+POMDPSettings.LOSS_COMPROMISED / math.pow(POMDPSettings.DISTANCE_FACTOR,
                                                                      distance_from_target)
    print('Node Values %s'%(POMDPSettings.node_values))

def recursive_child_value_upated(node,explored_node):
    this_value = 0
    for child in POMDPSettings.parent_nodes_considered_paths[node]:
            if child in explored_node:
                this_value += explored_node[child]
            else:
                this_value += recursive_child_value_upated(child,explored_node)
    target = POMDPSettings.target_node[0]
    distance_from_target = POMDPSettings.all_pair_shortest_path[target][node]
    explored_node[node] = this_value + POMDPSettings.LOSS_COMPROMISED / math.pow(POMDPSettings.DISTANCE_FACTOR,
                                                                                 distance_from_target)
    return explored_node[node]

def adversary_probability_update():
    '''Calculate the probability of forwarding from the nodes of the old states'''
    POMDPSettings.adversary_state_to_state_probability.clear()

    for old_state_id in POMDPSettings.state_transition_with_adversary:
        old_state = POMDPSettings.state_space[old_state_id]
        number_available_positions = len(old_state.adversary_positions)
        POMDPSettings.adversary_state_to_state_probability[old_state_id] = {}
        for new_state_id in POMDPSettings.state_transition_with_adversary[old_state_id]:
            new_state=POMDPSettings.state_space[new_state_id]
            POMDPSettings.adversary_state_to_state_probability[old_state_id][new_state_id] = 0.0
            for node in new_state.adversary_positions:
                if node <0:
                    node = -node
                number_ancestor = len(set(POMDPSettings.parent_nodes_considered_paths[node]) & set(old_state.adversary_positions)) # Check how may parent matches
                if number_ancestor > 0:
                    mirror_node = len([1 for parent in old_state.adversary_positions if parent < 0])
                    if mirror_node > 0: # Adversary will not forward from mirror Nodes
                        each_node_propagation_prob = 1.0/(number_available_positions-mirror_node)
                    else:
                        each_node_propagation_prob = 1.0 / number_available_positions
                    POMDPSettings.adversary_state_to_state_probability[old_state_id][new_state_id] += each_node_propagation_prob*number_ancestor

    # print('******** Probability of Forwarding from a state %s ******' % (POMDPSettings.adversary_state_to_state_probability))








