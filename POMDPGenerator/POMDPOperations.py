import POMDPSettings
from POMDPGenerator import POMDPComponentGenerator
import PrintLibrary,Utilities
import Dijkstra

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

    ############################################# Create the action space first ###############################
    POMDPComponentGenerator.initialize_action_space()


