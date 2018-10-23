import POMDPSettings
import ParseTopologyFile
import Dijkstra
import PrintLibrary,Utilities
from POMDPGenerator import POMDPOperations
from POMDPGenerator import POMDPModelGenerator

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
    # PrintLibrary.state_space_print(POMDPSettings.state_space,True)

    ######################################## Determine Discount factor #######################################
    POMDPOperations.determine_discount_factor()

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
    PrintLibrary.check_invalid_state_transition()

    #################################### Observation Matrix ############################################
    POMDPOperations.generate_observation_matrix()
    # PrintLibrary.observation_matrix()
    ################################ Rewards ##############################################################
    POMDPOperations.generate_reward()
    # PrintLibrary.rewards()

    PrintLibrary.generic_information()
    ################################ Generate Final Output Model ################################
    out_file = '%s/%s.pomdp'%(POMDPSettings.DIR_NAME,POMDPSettings.POMDP_MODEL_FILE_NAME)
    POMDPModelGenerator.generate_model(out_file)

    ############################ Calculate the precision ################################
    POMDPOperations.calculate_precision()

    ################################ Execute Action ##############################
    from POMDPActionExecutor import POMDPActionPlanner
    file_name = input("Enter the policy file location")
    file_name = 'InputFiles/Policies/mirror_4_final.policy'
    # print(file_name)
    POMDPActionPlanner.get_policy_functions(file_name)

    ###################### Recommended Actions ##############
    previous_action = POMDPActionPlanner.execute_action(POMDPSettings.current_belief)
    print('************* Execute Actions ********************')
    print(' Previous Actions :: %s' % (POMDPSettings.pomdp_policy_action_index[previous_action]))
    did = POMDPSettings.defense_action_id_to_position[POMDPSettings.pomdp_policy_action_index[previous_action]][0]
    dpos = POMDPSettings.defense_action_id_to_position[POMDPSettings.pomdp_policy_action_index[previous_action]][1]
    POMDPSettings.action_space_objects[did][dpos].printProperties()
    # while(True):
    #     print(' Previous Actions :: %s'%(previous_action))
    #     observations = input('Enter valid observations ')
    #     if observations==-1:
    #         break

if __name__=='__main__':
    print("Start of the CyberMirror Dynamic Planning")
    initilization()
    pomdp_engine()
