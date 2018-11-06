import math
import POMDPSettings
from POMDPGenerator import POMDPComponentGenerator
import PrintLibrary,Utilities
import Dijkstra
from Components import Actions
from Components import AdversaryAction
from CommonUtilities import DataStructureFunctions

def determine_discount_factor():
    # print(' *** All exploitable paths to target %s ***'%(POMDPSettings.possible_nodes_for_state))
    max_path = 0
    for path in POMDPSettings.possible_nodes_for_state:
        path_length = len(POMDPSettings.possible_nodes_for_state[path])
        if max_path < path_length:
            max_path = path_length
    ##### log10(M) = N ==> M = 10^N ##########################
    POMDPSettings.MAX_STEPS_TOPOLOGY = max_path
    N = math.log2(POMDPSettings.MINIMUM_FUTURE_WEIGHT)/max_path
    POMDPSettings.DISCOUNT_FACTOR = math.pow(2,N)
    print("**** Discount Factor %s ****"%(POMDPSettings.DISCOUNT_FACTOR))

def initialize_state_space_data_structure():
    del POMDPSettings.state_space[:]
    POMDPSettings.state_space_map.clear()
    POMDPSettings.possible_nodes_for_state.clear()

def determine_State_Space():
    initialize_state_space_data_structure()
    ####################################### State Space Determination #####################################################################
    ################### 1.1 First Find the shortest path ###############################################################
    for com_node in POMDPSettings.compromised_nodes_current_time:
        POMDPSettings.possible_nodes_for_state[com_node] = Dijkstra.shortest_route(com_node,POMDPSettings.target_node[0],POMDPSettings.adjacent_matrix)
        print("*************** Shortest Path from Source: %s to Destination : %s --> %s"
              "********************"%(com_node,POMDPSettings.target_node[0],POMDPSettings.possible_nodes_for_state[com_node]))
    ############## 1.2 Determine Possible State Space ##################################################################
    POMDPComponentGenerator.generate_initial_state_space(POMDPSettings.possible_nodes_for_state)

    ###################### 1.3 Determine their parent states ###############################################################
    POMDPComponentGenerator.update_state_value_from_leaves()
    for state in POMDPSettings.state_space:
        state.set_possible_parent_nodes()
        state.determine_state_value()


def determine_Initial_Belief():
    # print('************* Compromised Nodes :%s'%(POMDPSettings.compromised_nodes_current_time))
    # print('************* IDS Score :%s'%(POMDPSettings.compromised_nodes_probability))
    POMDPComponentGenerator.generate_initial_belief(POMDPSettings.compromised_nodes_current_time,
                                                    POMDPSettings.compromised_nodes_probability,
                                                    POMDPSettings.state_space,POMDPSettings.state_space_map)
    ############################### Normalize the initial belief ##########################################
    Utilities.normalize_state_probability(POMDPSettings.state_space)

def initialize_action_space_data_structure():
    del POMDPSettings.action_space_by_type[:]
    del POMDPSettings.action_space_all_values[:]
    POMDPSettings.action_space_group_index.clear()
    del POMDPSettings.action_space_objects[:]
    POMDPSettings.defense_action_id_to_position.clear()
    POMDPSettings.action_based_on_nodes.clear()

def determine_Action_Space():
    initialize_action_space_data_structure()
    possible_next_adv_position = set([])
    for node in POMDPSettings.possible_nodes_for_state:
        possible_next_adv_position |= set(POMDPSettings.possible_nodes_for_state[node][1:])
    # print('************ Possible Adversay Next Positions %s********'%(POMDPSettings.possible_nodes_for_state))

    POMDPSettings.next_adversary_nodes = list(possible_next_adv_position)
    if POMDPSettings.SORT_ADVERSARY_POSITION:
        POMDPSettings.next_adversary_nodes = sorted(POMDPSettings.next_adversary_nodes)
    print('************ Possible Nodes for Actions %s********' % (POMDPSettings.next_adversary_nodes))

    ############################################# Create the action space first ###############################
    Utilities.reachable_from_other_nodes()
    POMDPComponentGenerator.initialize_action_space()
    POMDPComponentGenerator.generate_action_space()
    POMDPComponentGenerator.set_weighted_cost_effectiveness_action_space()
    prune_action_space()

    ####################################### Add Do Nothing #############################
    print('Number of defense After Prunning %s'%(sum([len(POMDPSettings.action_space_objects[i]) for i in range(len(POMDPSettings.action_space_objects))])))
    index_id = 0
    for node in POMDPSettings.next_adversary_nodes:
        POMDPSettings.action_space_objects[index_id].append(
            Actions.Actions(POMDPSettings.DEFENSE_ACTION_TOTAL,node,POMDPSettings.DEFENSE_DO_NOTHING_ACTION))
        POMDPSettings.action_space_objects[index_id][-1].set_effectiveness()
        POMDPSettings.DEFENSE_ACTION_TOTAL += 1
        index_id += 1
    create_defense_id_map()

def prune_action_space():
    if POMDPSettings.MARGINAL_PRUNNING:
        POMDPComponentGenerator.marginal_prunning(POMDPSettings.action_space_objects)

    if POMDPSettings.IRRELEVANT_PRUNNING:
        POMDPComponentGenerator.irrelevant_prunning(POMDPSettings.action_space_objects)

    if POMDPSettings.REDUNDANT_PRUNNING:
        # print("****** Before Redundant Prunning ***************")
        # PrintLibrary.number_action_available_each_node(POMDPSettings.action_space_objects)
        index = 0
        for action_type in POMDPSettings.action_space_objects:
            POMDPSettings.action_space_objects[index] = POMDPComponentGenerator.redundant_prunning(action_type)
            index += 1
        # print("****** After Redundant Prunning ***************")
        # PrintLibrary.number_action_available_each_node(POMDPSettings.action_space_objects)

def create_defense_id_map():
    for i in range(len(POMDPSettings.action_space_objects)):
        index = 0
        for action in POMDPSettings.action_space_objects[i]:
            if action.node_id not in POMDPSettings.action_based_on_nodes:
                POMDPSettings.action_based_on_nodes[action.node_id] = []
            POMDPSettings.defense_action_id_to_position[action.primary_key] = [i,index]
            POMDPSettings.action_based_on_nodes[action.node_id].append([i,index])
            index += 1

def initialize_adversary_action_space_data_structure():
    del POMDPSettings.adversary_action_objects[:]
    POMDPSettings.adversary_action_id_to_position.clear()

def determine_adversary_action_space():
    initialize_adversary_action_space_data_structure()
    id = 0
    for position in range(len(POMDPSettings.compromised_nodes_current_time)):
        POMDPSettings.adversary_action_objects.append(
            AdversaryAction.Adversary_Action(id, False, False, POMDPSettings.ADVERSARY_DO_NOTHING,position))
        POMDPSettings.adversary_action_id_to_position[id] = id
        id += 1
        POMDPSettings.adversary_action_objects.append(
            AdversaryAction.Adversary_Action(id, True, True,
                                             POMDPSettings.ADVERSARY_ADVANCE * POMDPSettings.ADVERSARY_SCANNING_PROB,position))
        POMDPSettings.adversary_action_id_to_position[id] = id
        id += 1
        POMDPSettings.adversary_action_objects.append(
            AdversaryAction.Adversary_Action(id, False, True,
                                             POMDPSettings.ADVERSARY_ADVANCE * (1 - POMDPSettings.ADVERSARY_SCANNING_PROB),position))
        POMDPSettings.adversary_action_id_to_position[id] = id
        id += 1
        if POMDPSettings.ONE_ADVERSARY_UNIFORM_MOVEMENT:
            break
    # print("Adversarry : %s == %s"%(len(POMDPSettings.adversary_action_objects),POMDPSettings.adversary_action_id_to_position))


def initialize_state_transition_data_structure():
    POMDPSettings.state_transition_with_adversary.clear()
    POMDPSettings.state_transition_pomdp.clear()

def generate_state_transition():
    initialize_state_transition_data_structure()
    __generate_game_transition()

def __generate_game_transition():
    # print('************* Possible Adversary Action Space %s'%(POMDPSettings.possible_nodes_for_state))
    # PrintLibrary.state_space_print(POMDPSettings.state_space)
    # PrintLibrary.comprehensive_action_space_print(POMDPSettings.action_space_objects)
    # PrintLibrary.comprehensive_adversary_action_space(POMDPSettings.adversary_action_objects)
    # print('************* State Space Map %s **********'%(POMDPSettings.state_space_map))
    ###################### First consider the state transition ##################################
    ###################### 1.1 Determine State Transition with Adversary ##################################
    POMDPComponentGenerator.state_transition_initializations()
    # PrintLibrary.probability_forward_from_old_to_new()
    POMDPComponentGenerator.assign_state_transition_probability_with_adversary()
    # PrintLibrary.check_the_probability_transition(True)

    ###################### 1.2 Determine Expected State Transition for POMDP ##################################
    __generate_expected_behavior()
    # PrintLibrary.pomdp_expected_probability_transition()

def __generate_expected_behavior():
    ''' Generate the state transition for the POMDP Model'''
    for old_state_id in POMDPSettings.state_transition_with_adversary:
        old_state = POMDPSettings.state_space[old_state_id]
        #################################### New States ###################################
        for new_state_id in POMDPSettings.state_transition_with_adversary[old_state_id]:
            new_state = POMDPSettings.state_space[new_state_id]
            #################################### Defense Action ###################################
            for defense_action_id in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id]:
                ################################ Initialize such condition if does not exist #################
                if defense_action_id not in POMDPSettings.state_transition_pomdp:
                    POMDPSettings.state_transition_pomdp[defense_action_id] = {}
                if old_state_id not in POMDPSettings.state_transition_pomdp[defense_action_id]:
                    POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id] = {}
                if new_state_id not in POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id]:
                    POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id][new_state_id] = 0.0

                ################################ Adversary Actions #####################################
                for adversary_action_id in POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id]:
                    adversary = POMDPSettings.adversary_action_objects[adversary_action_id]
                    ######## Expected State Transition #################
                    POMDPSettings.state_transition_pomdp[defense_action_id][old_state_id][new_state_id] += \
                        POMDPSettings.state_transition_with_adversary[old_state_id][new_state_id][defense_action_id][adversary_action_id]\
                        *adversary.attack_probability
    DataStructureFunctions.normalize_probability_by_keys(POMDPSettings.state_transition_pomdp)

def initialize_observation_space_data_structure():
    POMDPSettings.observation_probability.clear()

def generate_observation_matrix():
    initialize_observation_space_data_structure()
    ''' Give the observation Matrix'''
    if POMDPSettings.OBSERVATION_ACTION_IRRESPECTIVE:
        POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL] = {}
        for old_state in POMDPSettings.state_space:
            if old_state.primary_key not in POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL]:
                POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key] = {}
            for new_state in POMDPSettings.state_space:
                if new_state.primary_key == old_state.primary_key:
                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][new_state.primary_key] \
                        = new_state.get_observation_probability()[0]
                else:
                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][
                        new_state.primary_key] \
                        = new_state.get_observation_probability()[1]
                    difference = set(old_state.adversary_positions) & set(new_state.adversary_positions)
                    for node in difference:
                        if node < 0:
                            POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][
                                new_state.primary_key] /= POMDPSettings.MIRROR_NODE_FALSE_POSITIVE
                            POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][
                                new_state.primary_key] *= POMDPSettings.MIRROR_NODE_TRUE_POSITIVE
                        else:
                            POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][
                                new_state.primary_key] /= POMDPSettings.IDS_FALSE_POSITIVE
                            POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][old_state.primary_key][
                                new_state.primary_key] *= POMDPSettings.IDS_TRUE_POSITIVE_RATE
    else:
        for defense_type in POMDPSettings.action_space_objects:
            for defense in defense_type:
                if defense.primary_key not in POMDPSettings.observation_probability:
                    POMDPSettings.observation_probability[defense.primary_key] = {}
                for old_state in POMDPSettings.state_space:
                    if old_state.primary_key not in POMDPSettings.observation_probability[defense.primary_key]:
                        POMDPSettings.observation_probability[defense.primary_key][old_state.primary_key] = {}
                    for new_state in POMDPSettings.state_space: ###### This is actually for observation ################
                        if new_state.primary_key == old_state.primary_key:
                            POMDPSettings.observation_probability[defense.primary_key][old_state.primary_key][new_state.primary_key] \
                                = new_state.get_observation_probability()[0]
                        else:
                            POMDPSettings.observation_probability[defense.primary_key][old_state.primary_key][
                                new_state.primary_key] \
                                = new_state.get_observation_probability()[1]
                            difference = set(old_state.adversary_positions) & set(new_state.adversary_positions)
                            for node in difference:
                                if node < 0:
                                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][
                                        old_state.primary_key][
                                        new_state.primary_key] /= POMDPSettings.MIRROR_NODE_FALSE_POSITIVE
                                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][
                                        old_state.primary_key][
                                        new_state.primary_key] *= POMDPSettings.MIRROR_NODE_TRUE_POSITIVE
                                else:
                                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][
                                        old_state.primary_key][
                                        new_state.primary_key] /= POMDPSettings.IDS_FALSE_POSITIVE
                                    POMDPSettings.observation_probability[POMDPSettings.WILDCARD_SYMBOL][
                                        old_state.primary_key][
                                        new_state.primary_key] *= POMDPSettings.IDS_TRUE_POSITIVE_RATE
    DataStructureFunctions.normalize_probability_by_keys(POMDPSettings.observation_probability)

def generate_reward():
    ''' Generate the rewards for the POMDP Model'''
    POMDPSettings.rewards_pomdp.clear()  ############### Generate Rewards POMDP #####################
    for old_state in POMDPSettings.state_space:
        old_state_id = old_state.primary_key
        if old_state_id not in POMDPSettings.rewards_pomdp:
            POMDPSettings.rewards_pomdp[old_state_id] = {}
        #################################### New States ###################################
        for new_state in POMDPSettings.state_space:
            new_state_id = new_state.primary_key
            if new_state_id not in POMDPSettings.rewards_pomdp[old_state_id]:
                POMDPSettings.rewards_pomdp[old_state_id][new_state_id] = {}
            #################################### Defense Action ###################################
            for defense_type in POMDPSettings.action_space_objects:
                for defense_action in defense_type:
                    ################################ Initialize such condition if does not exist #################
                    reward_without_adversary_cost = new_state.state_value - old_state.state_value - defense_action.cost
                    if new_state_id==old_state_id and new_state_id not in POMDPSettings.target_node:
                        if len(set(POMDPSettings.parent_nodes_considered_paths[defense_action.node_id]) & set(old_state.adversary_positions)) > 0:
                            # print('Add reward Defense Node %s:%s Current State %s'%(defense_action.node_id,defense_action.primary_key,old_state.adversary_positions))
                            reward_without_adversary_cost += POMDPSettings.GAIN_HONEYPOT
                    defense_action_id = defense_action.primary_key
                    if defense_action_id not in POMDPSettings.rewards_pomdp[old_state_id][new_state_id]:
                        POMDPSettings.rewards_pomdp[old_state_id][new_state_id][defense_action_id] = {}
                    ################################ Observation Probability ##############################
                    if POMDPSettings.PENALTY_WRONG_OBSERVATION:
                        pass
                    else:
                        POMDPSettings.rewards_pomdp[old_state_id][new_state_id][defense_action_id][POMDPSettings.WILDCARD_SYMBOL] = 0.0
                        ################################ Adversary Actions #####################################
                        for adversary in POMDPSettings.adversary_action_objects:
                            ############# Generated Rewards ###############
                            POMDPSettings.rewards_pomdp[old_state_id][new_state_id][
                                defense_action_id][POMDPSettings.WILDCARD_SYMBOL] += (reward_without_adversary_cost-adversary.adv_cost)*adversary.attack_probability

    # DataStructureFunctions.normalize_probability_by_max_or_min(data_structure=POMDPSettings.rewards_pomdp,abs_value=True,by_max=True)

def calculate_precision():
    ########################### Find the action with maximum reward ################################
    max_reward = DataStructureFunctions.find_max_or_min_of_dictionary(POMDPSettings.rewards_pomdp,max_flag=True)
    print('Max Number of Steps %s'%(POMDPSettings.MAX_STEPS_TOPOLOGY))
    POMDPSettings.POMDP_PRECISION = max_reward
    current_value = max_reward
    while True:
        current_value *= POMDPSettings.DISCOUNT_FACTOR
        if current_value <= 0.001:
            break
        # print(current_value)
        POMDPSettings.POMDP_PRECISION += current_value
    POMDPSettings.POMDP_PRECISION *= POMDPSettings.REGRET_PERCENTAGE
    print('********* Precision %s'%(POMDPSettings.POMDP_PRECISION))

def __update_defense_assessment(node_id,recommended_action):
    if node_id not in POMDPSettings.deployed_defense_assessment:
        POMDPSettings.deployed_defense_assessment[node_id] = [0.0,0.0]
    POMDPSettings.deployed_defense_assessment[node_id][0] = recommended_action.effeciveness_with_scan
    POMDPSettings.deployed_defense_assessment[node_id][1] = recommended_action.effeciveness_without_scan

def implement_executed_action(recommended_action):
    '''Implement the recommended executed action'''
    node_id = recommended_action.node_id
    ###### Initialize the defense plan for the node #############
    if node_id not in POMDPSettings.deployed_defense_nodes:
        POMDPSettings.deployed_defense_nodes[node_id] = {}
        if POMDPSettings.SPATIAL_MUTATION_ENABLED:
            POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.SPATIAL_MUTATION_INDEX] = 1.0
        if POMDPSettings.TEMPORAL_MUTATION_ENABLED:
            POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.TEMPORAL_MUTATION_INDEX] = 0.0
        if POMDPSettings.DIVERSITY_ENABLED:
            POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.DIVERSITY_INDEX] = 1.0
        if POMDPSettings.ANONYMIZATION_ENABLED:
            POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.ANONYMIZATION_INDEX] = 1.0

    ####################### Insert the values ##########################################
    if POMDPSettings.SPATIAL_MUTATION_ENABLED:
        POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.SPATIAL_MUTATION_INDEX] = recommended_action.spatial_mutation
        POMDPSettings.MAX_AVAILABLE_IP_ADDRESS -= recommended_action.spatial_ip_number
    if POMDPSettings.TEMPORAL_MUTATION_ENABLED:
        POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.TEMPORAL_MUTATION_INDEX] = recommended_action.temporal_mutation
    if POMDPSettings.DIVERSITY_ENABLED:
        POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.DIVERSITY_INDEX] += recommended_action.diversity-1
    if POMDPSettings.ANONYMIZATION_ENABLED:
        POMDPSettings.deployed_defense_nodes[node_id][POMDPSettings.ANONYMIZATION_INDEX] += recommended_action.anonymization-1
        POMDPSettings.MAX_AVAILABLE_ANONYMITY -= recommended_action.anonymization - 1

    __update_defense_assessment(node_id,recommended_action)



