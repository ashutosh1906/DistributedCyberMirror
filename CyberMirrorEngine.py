import POMDPSettings
import ParseTopologyFile
import Dijkstra
import PrintLibrary,Utilities
from POMDPGenerator import POMDPOperations


def initilization():
    print('Initialize the environment')
    ParseTopologyFile.parse_aSHIIP_topology_bi_directional(POMDPSettings.TOPOLOGY_FILE_NAME, POMDPSettings.adjacent_matrix)
    if POMDPSettings.USER_INPUT_TARGET_NODE:
        while(True):
            print("Please enter the target node. Any number between [0-%s]"%(len(POMDPSettings.adjacent_matrix)-1))
            user_input_target_node = int(input())
            if user_input_target_node > len(POMDPSettings.adjacent_matrix)-1:
                print("No Such Node. Please try again")
                continue
            POMDPSettings.target_node.append(user_input_target_node) ########### Assuming one target node currently, so index will be 0
            break
    else:
        POMDPSettings.target_node = POMDPSettings.STATIC_TARGET_NODE
    print("Target Node : %s"%(POMDPSettings.target_node))

    ############################################# Now we are assuming just one target for each POMDP agent #############################
    target_resource = POMDPSettings.target_node[0]
    POMDPSettings.all_pair_shortest_path[target_resource] = Dijkstra.Dijkstra_algorithm_unweighted(target_resource,POMDPSettings.adjacent_matrix)
    PrintLibrary.all_pair_shortest_path_print(POMDPSettings.all_pair_shortest_path)  ######## Print the shortest path knowledge #############

    ######################################### Get the IDS score of the compromised nodes with non_zero probability ##############################
    Utilities.get_compromised_nodes(0,POMDPSettings.compromised_nodes_probability)
    Utilities.calculate_score_compromised_nodes(POMDPSettings.compromised_nodes_probability,
                                                POMDPSettings.impact_nodes,POMDPSettings.all_pair_shortest_path)
    PrintLibrary.score_compromised_node(POMDPSettings.impact_nodes)
    POMDPSettings.compromised_nodes_current_time = Utilities.select_compromised_nodes(POMDPSettings.impact_nodes)
    print("***************** Selected Compromised Nodes %s*************************" % (POMDPSettings.compromised_nodes_current_time))


def pomdp_engine():
    ######################################### Create State Space ##############################################
    POMDPOperations.determine_State_Space()
    PrintLibrary.state_space_print(POMDPSettings.state_space,True)

    ######################################## Initial Belief ###################################################
    POMDPOperations.determine_Initial_Belief()
    # PrintLibrary.state_space_print(POMDPSettings.state_space)

    ####################################### Action Space ######################################################
    POMDPOperations.determine_Action_Space()
    # PrintLibrary.action_space_type_Print(POMDPSettings.action_space_by_type,POMDPSettings.action_space_group_index)
    # PrintLibrary.action_space_Print(POMDPSettings.action_space_all_values,
    #                                 POMDPSettings.compromised_nodes_current_time,POMDPSettings.next_adversary_nodes,print_each_action=False)
    # PrintLibrary.comprehensive_action_space_print(POMDPSettings.action_space_objects)

    ################################# Adversary Action ######################################################
    POMDPOperations.determine_adversary_action_space()
    # PrintLibrary.comprehensive_adversary_action_space(POMDPSettings.adversary_action_objects)
    # PrintLibrary.comprehensive_adversary_action_space(POMDPSettings.adversary_action_objects)
    # PrintLibrary.generic_information()

    ############################### State Transition #########################################################
    POMDPOperations.generate_state_transition()

if __name__=='__main__':
    print("Start of the CyberMirror Dynamic Planning")
    initilization()
    pomdp_engine()
