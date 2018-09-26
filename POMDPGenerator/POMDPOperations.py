import POMDPSettings
from POMDPGenerator import POMDPComponentGenerator
import PrintLibrary
import Dijkstra

def determine_state_space():
    del POMDPSettings.state_space[:]
    POMDPSettings.state_space_map.clear()
    ####################################### State Space Determination #####################################################################
    ################### 1.1 First Find the shortest path ###############################################################
    possible_nodes_for_state = {}
    for com_node in POMDPSettings.compromised_nodes_current_time:
        possible_nodes_for_state[com_node] = Dijkstra.shortest_route(com_node,POMDPSettings.target_node[0],POMDPSettings.adjacent_matrix)
        print("*************** Shortest Path from Source: %s to Destination : %s --> %s"
              "********************"%(com_node,POMDPSettings.target_node[0],possible_nodes_for_state[com_node]))
    ############## 1.2 Determine Possible State Space ##################################################################
    POMDPComponentGenerator.generate_initial_state_space(possible_nodes_for_state)


def determine_initial_belief():
    # print('************* Compromised Nodes :%s'%(POMDPSettings.compromised_nodes_current_time))
    # print('************* IDS Score :%s'%(POMDPSettings.compromised_nodes_probability))

