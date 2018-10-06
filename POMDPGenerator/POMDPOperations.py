import POMDPSettings
from POMDPGenerator import POMDPComponentGenerator
import PrintLibrary,Utilities
import Dijkstra
from Components import Actions
from Components import AdversaryAction

def determine_State_Space():
    del POMDPSettings.state_space[:]
    POMDPSettings.state_space_map.clear()
    ####################################### State Space Determination #####################################################################
    ################### 1.1 First Find the shortest path ###############################################################
    for com_node in POMDPSettings.compromised_nodes_current_time:
        POMDPSettings.possible_nodes_for_state[com_node] = Dijkstra.shortest_route(com_node,POMDPSettings.target_node[0],POMDPSettings.adjacent_matrix)
        print("*************** Shortest Path from Source: %s to Destination : %s --> %s"
              "********************"%(com_node,POMDPSettings.target_node[0],POMDPSettings.possible_nodes_for_state[com_node]))
    ############## 1.2 Determine Possible State Space ##################################################################
    POMDPComponentGenerator.generate_initial_state_space(POMDPSettings.possible_nodes_for_state)


def determine_Initial_Belief():
    # print('************* Compromised Nodes :%s'%(POMDPSettings.compromised_nodes_current_time))
    # print('************* IDS Score :%s'%(POMDPSettings.compromised_nodes_probability))
    POMDPComponentGenerator.generate_initial_belief(POMDPSettings.compromised_nodes_current_time,
                                                    POMDPSettings.compromised_nodes_probability,
                                                    POMDPSettings.state_space,POMDPSettings.state_space_map)
    ############################### Normalize the initial belief ##########################################
    Utilities.normalize_state_probability(POMDPSettings.state_space)

def determine_Action_Space():
    possible_next_adv_position = set([])
    for node in POMDPSettings.possible_nodes_for_state:
        possible_next_adv_position |= set(POMDPSettings.possible_nodes_for_state[node][1:])
    print('************ Possible Adversay Next Positions %s********'%(POMDPSettings.possible_nodes_for_state))
    print('************ Possible Nodes for Actions %s********' % (possible_next_adv_position))
    POMDPSettings.next_adversary_nodes = list(possible_next_adv_position)

    ############################################# Create the action space first ###############################
    Utilities.reachable_from_other_nodes()
    POMDPComponentGenerator.initialize_action_space()
    POMDPComponentGenerator.generate_action_space()
    prune_action_space()

    ####################################### Add Do Nothing #############################
    # print('Number of defense %s'%(POMDPSettings.DEFENSE_ACTION_TOTAL))
    index_id = 0
    for node in POMDPSettings.next_adversary_nodes:
        POMDPSettings.action_space_objects[index_id].append(
            Actions.Actions(POMDPSettings.DEFENSE_ACTION_TOTAL,node,POMDPSettings.DEFENSE_DO_NOTHING_ACTION))
        POMDPSettings.DEFENSE_ACTION_TOTAL += 1
        index_id += 1
    create_defense_id_map()

def prune_action_space():
    if POMDPSettings.MARGINAL_PRUNNING:
        POMDPComponentGenerator.marginal_prunning(POMDPSettings.action_space_objects)

    if POMDPSettings.REDUNDANT_PRUNNING:
        print("****** Before Redundant Prunning ***************")
        PrintLibrary.number_action_available_each_node(POMDPSettings.action_space_objects)
        index = 0
        for action_type in POMDPSettings.action_space_objects:
            POMDPSettings.action_space_objects[index] = POMDPComponentGenerator.redundant_prunning(action_type)
            index += 1
        print("****** After Redundant Prunning ***************")
        PrintLibrary.number_action_available_each_node(POMDPSettings.action_space_objects)

    if POMDPSettings.IRRELEVANT_PRUNNING:
        POMDPComponentGenerator.irrelevant_prunning(POMDPSettings.action_space_objects)

def determine_adversary_action_space():
    id = 0
    POMDPSettings.adversary_action_id_to_position.clear()
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

def create_defense_id_map():
    POMDPSettings.defense_action_id_to_position.clear()
    for i in range(len(POMDPSettings.action_space_objects)):
        index = 0
        for action in POMDPSettings.action_space_objects[i]:
            POMDPSettings.defense_action_id_to_position[action.primary_key] = [i,index]
            index += 1






