import POMDPSettings
import ParseTopologyFile
import Dijkstra
import PrintLibrary,Utilities
from POMDPGenerator import POMDPOperations
from POMDPGenerator import POMDPModelGenerator

def dynamic_planning_initialization(time_sequence,calculate_compromised_nodes=True):
    print('\n\n************************** Start Planning for time %s *********************************'%(time_sequence))
    ######################################### Get the IDS score of the compromised nodes with non_zero probability ##############################
    if calculate_compromised_nodes:
        Utilities.get_compromised_nodes(time_sequence,POMDPSettings.compromised_nodes_probability)
    Utilities.calculate_score_compromised_nodes(POMDPSettings.compromised_nodes_probability,
                                                POMDPSettings.impact_nodes, POMDPSettings.all_pair_shortest_path)
    PrintLibrary.score_compromised_node(POMDPSettings.impact_nodes)
    POMDPSettings.compromised_nodes_current_time = Utilities.select_compromised_nodes(POMDPSettings.impact_nodes)
    POMDPSettings.compromised_nodes_current_time = sorted(POMDPSettings.compromised_nodes_current_time)
    print("***************** Selected Compromised Nodes %s*************************" % (
        POMDPSettings.compromised_nodes_current_time))

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
    print('******* End of static environment initialization ***************')

def pomdp_engine():
    ######################################### Create State Space ##############################################
    POMDPOperations.determine_State_Space()
    # PrintLibrary.state_space_print(POMDPSettings.state_space,True)
    print('State Space Map %s'%(POMDPSettings.state_space_map))
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
    # PrintLibrary.generic_information()
    #################################### Observation Matrix ############################################
    POMDPOperations.generate_observation_matrix()
    # PrintLibrary.observation_matrix()
    # PrintLibrary.generic_information()
    ################################ Rewards ##############################################################
    POMDPOperations.generate_reward()
    # PrintLibrary.rewards()

    PrintLibrary.generic_information()
    ################################ Generate Final Output Model ################################
    out_file = '%s/%s.pomdp'%(POMDPSettings.DIR_NAME,POMDPSettings.POMDP_MODEL_FILE_NAME)
    if POMDPSettings.POMDP_FILE_FAST_PARSING:
        POMDPModelGenerator.generate_model_fast_parsing(out_file)
    else:
        POMDPModelGenerator.generate_model(out_file)

    ############################ Calculate the precision ################################
    POMDPOperations.calculate_precision()

    ################## Solve the POMDP Model ##############################
    print("POMDP Model %s" % (out_file))
    print("Policy File Name %s"%(POMDPSettings.POMDP_POLICY_FILE_NAME))
    generate_policy_cmd = '%s solve -f -o %s -p %s %s'%(POMDPSettings.ZMDP_EXECUTOR,
                                                    POMDPSettings.POMDP_POLICY_FILE_NAME,POMDPSettings.POMDP_PRECISION,out_file)
    print(generate_policy_cmd)
    import os
    os.system(generate_policy_cmd)

    ################################ Execute Action ##############################
    from POMDPActionExecutor import POMDPActionPlanner
    # file_name = input("Enter the policy file location ")
    # file_name = '%s/%s.policy'%(POMDPSettings.POLICY_FILE_GENERATED,file_name)
    POMDPActionPlanner.get_policy_functions(POMDPSettings.POMDP_POLICY_FILE_NAME)

    ###################### Recommended Actions ##############
    previous_action = POMDPActionPlanner.execute_action(POMDPSettings.current_belief)
    print('************* Execute Actions ********************')
    print(' Previous Actions :: %s' % (POMDPSettings.pomdp_policy_action_index[previous_action]))
    did = POMDPSettings.defense_action_id_to_position[POMDPSettings.pomdp_policy_action_index[previous_action]][0]
    dpos = POMDPSettings.defense_action_id_to_position[POMDPSettings.pomdp_policy_action_index[previous_action]][1]
    POMDPSettings.action_space_objects[did][dpos].printProperties()
    POMDPOperations.implement_executed_action(POMDPSettings.action_space_objects[did][dpos])
    # PrintLibrary.defense_planning(time_sequence,POMDPSettings.deployed_defense_nodes)
    Utilities.write_defense_planning_in_file(time_sequence,POMDPSettings.deployed_defense_nodes,
                                             file_name='%s/%s'%(POMDPSettings.OUT_DIR_CONCEAL,POMDPSettings.OUT_DEFENSE_PLAN_FILE))


def next_compromised_nodes():
    print('Check(2) :: Current Compromised %s'%(POMDPSettings.compromised_nodes_current_time))
    print('Next Possible Nodes %s'%(POMDPSettings.possible_nodes_for_state))
    print('Possible States %s'%(POMDPSettings.state_space_map))
    current_state = POMDPSettings.state_space_map[tuple(POMDPSettings.compromised_nodes_current_time)]
    # print('Defense at Nodes %s'%(POMDPSettings.deployed_defense_assessment))
    # print('Parent Nodes %s'%(POMDPSettings.parent_nodes_of_each_node))
    # print('Compromised Nodes Probability %s'%(POMDPSettings.compromised_nodes_probability))
    # print('Impact Nodes %s'%(POMDPSettings.impact_nodes))
    for state in POMDPSettings.state_space:
        if current_state in state.parent_states:
            # print('\t Adv. Positions %s'%(POMDPSettings.state_space[state.primary_key].adversary_positions),end='')
            # print(' Probability %s'%(POMDPSettings.adversary_state_to_state_probability[current_state][state.primary_key]))
            for adv_position in state.adversary_positions:
                if adv_position not in POMDPSettings.state_space[current_state].adversary_positions:
                    POMDPSettings.compromised_nodes_probability[adv_position] = 1.0
                    if adv_position in POMDPSettings.deployed_defense_assessment:
                        POMDPSettings.compromised_nodes_probability[adv_position] = POMDPSettings.ADVERSARY_SCANNING_PROB*\
                                                                                    (1-POMDPSettings.deployed_defense_assessment[adv_position][0]) ## Effectiveness with scan
                        POMDPSettings.compromised_nodes_probability[adv_position] += (1-POMDPSettings.ADVERSARY_SCANNING_PROB)\
                                                                                    *(1-POMDPSettings.deployed_defense_assessment[adv_position][1]) ## Effectiveness without scan
                    POMDPSettings.compromised_nodes_probability[adv_position] *= POMDPSettings.adversary_state_to_state_probability[current_state][state.primary_key]\
                                                                                 *POMDPSettings.state_space[current_state].belief
    print('Compromised Nodes Probability %s' % (POMDPSettings.compromised_nodes_probability))

def evaluation(time_sequence):
    while (True):
        dynamic_planning_initialization(time_sequence, calculate_compromised_nodes=True)
        pomdp_engine()
        time_sequence += 1
        print('\n ****** Deployed Defense \n\t%s\n\t%s'%(POMDPSettings.deployed_defense_nodes,POMDPSettings.deployed_defense_assessment))
        next_compromised_nodes()
        continue_evaluation = input('\nDo you wish to continue? Press 1 if yes and 0 otherwise ')
        if continue_evaluation == '0':
            break

    if POMDPSettings.target_node[0] in POMDPSettings.compromised_nodes_probability:
        print(' Success Probability to compromise Target=%s is %s'%(POMDPSettings.target_node[0],
                                                                    POMDPSettings.compromised_nodes_probability[POMDPSettings.target_node[0]]*POMDPSettings.ADVERSARY_ADVANCE
                                                                    ))

if __name__=='__main__':
    print("Start of the CyberMirror Dynamic Planning")
    initilization()
    time_sequence = 0
    if POMDPSettings.EVALUATION_PROCESS:
        evaluation(time_sequence)
    else:
        while (True):
            dynamic_planning_initialization(time_sequence,calculate_compromised_nodes=True)
            pomdp_engine()
            time_sequence += 1
            print('Deployed Defense %s\n\t%s' % (
            POMDPSettings.deployed_defense_nodes, POMDPSettings.deployed_defense_assessment))
            continue_evaluation = input('Do you wish to continue? Press 1 if yes and 0 otherwise ')
            if continue_evaluation == '0':
                break



