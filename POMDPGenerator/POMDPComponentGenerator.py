from Components import State,Actions
import POMDPSettings
from CommonUtilities import SetOperations
from CommonUtilities import DataStructureFunctions
import Utilities,PrintLibrary
import random
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
    PrintLibrary.possible_combinations_print(possible_node_combinations, 'Nodes Positions')
    if POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
        POMDPSettings.possible_node_combinations = create_mirror_corresponding_nodes(possible_node_combinations)
    else:
        POMDPSettings.possible_node_combinations = possible_node_combinations
    PrintLibrary.possible_combinations_print(POMDPSettings.possible_node_combinations, 'Nodes Positions')
    ######################### Generate States ####################################
    determine_parent_nodes()
    state_id = 0
    del POMDPSettings.state_space[:]
    for adv_positions in POMDPSettings.possible_node_combinations:
        if POMDPSettings.SORT_ADVERSARY_POSITION:
            adv_positions = sorted(adv_positions)
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
    print('Possible Nodes for State %s'%(POMDPSettings.possible_nodes_for_state))
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
    print('Parent %s'%(POMDPSettings.parent_nodes_considered_paths))

# def iterate_over_possible_state(adv_position_node,current_depth,max_depth,chosen_node):
#     # print('Current Depth %s Chosen Nodes %s'%(current_depth,chosen_node))
#     if current_depth > max_depth:
#         return
#     if current_depth==max_depth:
#         state_id = len(POMDPSettings.state_space)
#         for node in adv_position_node[current_depth-1]:
#             current_state = []
#             for i in chosen_node:
#                 current_state.append(i)
#             current_state.append(node)
#             POMDPSettings.state_space.append(State.State(state_id,current_state))
#             POMDPSettings.state_space_map[tuple(current_state)] = state_id
#             state_id += 1
#             # print("\t Current State is %s"%(current_state))
#         return
#     for node in adv_position_node[current_depth-1]:
#         current_state = []
#         for i in chosen_node:
#             current_state.append(i)
#         current_state.append(node)
#         iterate_over_possible_state(adv_position_node,current_depth+1,max_depth,current_state)

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
    chosen_node.append(-first_adv_position)
    iterate_over_possible_belief(compromised_nodes_current_time, compromised_nodes_probability,
                                current_depth + 1,
                                chosen_node,state_space,state_space_map)
    del chosen_node[-1]

def generate_initial_belief(compromised_nodes_current_time,compromised_nodes_probability,state_space,state_space_map):
    print('***** Selectected Compromised Nodes %s'%(compromised_nodes_current_time))
    print('***** Selectected Compromised Nodes Prob %s' % (compromised_nodes_probability))
    print('******* State Space ************** %s'%(len(state_space)))
    print('******* State Space Map ************** %s' % (state_space_map))
    iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,
                                 1,[],state_space,state_space_map)


def initialize_action_space():
    index = 0
    del POMDPSettings.action_space_by_type[:]
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

    del POMDPSettings.action_space_all_values[:]
    POMDPSettings.action_space_all_values = \
        SetOperations.combination_possible_values_all_positions(POMDPSettings.action_space_by_type)

def generate_action_space():
    del POMDPSettings.action_space_objects[:]
    id = 0
    node_id = 0
    for node in POMDPSettings.next_adversary_nodes:
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

def marginal_prunning(action_space_objects):
    # print("***** Before Marginal Prunning Number of Actions ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)
    list_of_remove = []
    for node_index in range(len(action_space_objects)):
        for index in range(len(action_space_objects[node_index])):
            action = action_space_objects[node_index][index]
            # action.printProperties()
            if action.effeciveness_with_scan < POMDPSettings.MINIMUM_EFFECTIVENESS_WITH_SCAN:
                list_of_remove.append(index)
                # print("Pruned Out : Action Effectiveness with Scan %s"%(action.effeciveness_with_scan))
                continue
            if action.effeciveness_without_scan < POMDPSettings.MINIMUM_EFFECTIVENESS_WITHOUT_SCAN:
                list_of_remove.append(index)
                # print("Pruned Out : Action Effectiveness without Scan %s" % (action.effeciveness_without_scan))
                continue
        DataStructureFunctions.delete_values_by_index_from_list(POMDPSettings.action_space_objects[node_index],list_of_remove)
    # print("***** After Marginal Prunning Number of Actions ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)

def redundant_prunning(action_space_objects):
    # print("****** Before Redundant Prunning %s******"%(len(action_space_objects)))
    weighted_effectiveness_action = [] ###### Index of a value in this list is also representing the index in the action space
    weighted_cost_effectiveness_action = []
    for action in action_space_objects:
        weighted_effectiveness_action.append(0.0)
        weighted_effectiveness_action[-1] += POMDPSettings.ADVERSARY_SCANNING_PROB*action.effeciveness_with_scan
        weighted_effectiveness_action[-1] += (1-POMDPSettings.ADVERSARY_SCANNING_PROB) * action.effeciveness_without_scan
        action.set_weighted_effectiveness(weighted_effectiveness_action[-1])
        if POMDPSettings.Y_AXIS_COST_EFFECTIVENESS:
            weighted_cost_effectiveness_action.append(weighted_effectiveness_action[-1]*100/action.cost)
            action.set_weighted_cost_effectiveness(weighted_cost_effectiveness_action[-1])
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
                if current_effectiveness < seen_effectiveness[-1]:
                    delete_element.append(current_id)
                else:
                    seen_effectiveness.append(current_effectiveness)
        # print(seen_effectiveness)
        # print('Delete %s'%(delete_element))
        DataStructureFunctions.delete_values_by_index_from_list(action_space_objects[node_index],delete_element)

    # print("****** After Irrelevant Prunning ******")
    # PrintLibrary.number_action_available_each_node(action_space_objects)

################################################# Related to State Transition ##################################################
def state_transition_from_parent_nodes():
    ######## Previous State (key)---> Next State (Value) ###########################
    non_zero_transition = 0
    for new_state in POMDPSettings.state_space:
        new_state_id = POMDPSettings.state_space_map[tuple(new_state.adversary_positions)]
        for i in range(len(new_state.parent_nodes)):
            for list_parent in new_state.parent_nodes[i]:
                parent_id = POMDPSettings.state_space_map[tuple(list_parent)]
                if parent_id not in POMDPSettings.state_transition:
                    POMDPSettings.state_transition[parent_id] = {}
                POMDPSettings.state_transition[parent_id][new_state_id] = {}
                for node in new_state.adversary_positions:
                    if node in POMDPSettings.action_based_on_nodes:
                        # print('\t Applicable Actions of Node %s --> %s'%(node,POMDPSettings.action_based_on_nodes[node]))
                        for action_first_dimension,action_sec_dimension in POMDPSettings.action_based_on_nodes[node]:
                            id_to_action = POMDPSettings.action_space_objects[action_first_dimension][action_sec_dimension].primary_key
                            # print('****** Parent ID --> State ID --> Defense ID (%s,%s,%s)' % (parent_id, new_state_id,id_to_action))
                            non_zero_transition += 1
    print('*************** Non Zero Transitions %s*****************'%(non_zero_transition))





