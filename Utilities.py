import POMDPSettings
import random

def calculate_node_impact():
    ###################################### We will calculate the impact of the node here ###################
    ####################################### Temporary Random Process where impact is randonly considered between [0-5000]#######################################
    return random.randint(0,5000)

def get_impact_values(node_id):
    if node_id not in POMDPSettings.impact_nodes:
        ########################## Calculate the impact of the node #######################
        POMDPSettings.impact_nodes[node_id] = calculate_node_impact()
    return POMDPSettings.impact_nodes[node_id]


def calculate_score_compromised_nodes(compromised_nodes_probability,compromised_nodes_ids_score,all_pair_shortest_path):
    '''Calculate the score of a compromised host based on the IDS score, distance and the impact'''
    '''Impact depepends on both the centrality and the utility value of the resource'''
    print('********** Calculating the score of the compromised hosts ************************')
    print('\t Selected nodes are less than the depth : %s'%(POMDPSettings.MAXIMUM_DEPTH))
    for node in compromised_nodes_probability:
        if node in all_pair_shortest_path[POMDPSettings.target_node[0]]:
            if POMDPSettings.MAXIMUM_DEPTH_CHECK:
                if all_pair_shortest_path[POMDPSettings.target_node[0]][node] > POMDPSettings.MAXIMUM_DEPTH:
                    continue
            compromised_nodes_ids_score[node] = compromised_nodes_probability[node]\
                                                *get_impact_values(node)/all_pair_shortest_path[POMDPSettings.target_node[0]][node]

def get_compromised_nodes(time_sequence,compromised_nodes_probability):
    '''Get the IDS score for the possible compromised nodes where time sequence represents the period'''
    compromised_nodes_probability.clear()
    if POMDPSettings.READ_IDS_FROM_FILES:
        file_pointer = open(POMDPSettings.ADVERSARY_LOGS)
        for line in file_pointer:
            line = line.replace('\n','').split(',')
            compromised_node = int(line[0])
            compromise_probability = float(line[1])
            compromised_nodes_probability[compromised_node] = compromise_probability
            if POMDPSettings.READ_IMPACT_FROM_FILE:
                POMDPSettings.impact_nodes[compromised_node] = float(line[2])
        file_pointer.close()

def select_compromised_nodes(impact_nodes):
    compromised_nodes = None
    if POMDPSettings.COMPROMISED_NODES_SELECTION_ON_THRESHOLD:
        compromised_nodes = [i for i in impact_nodes if impact_nodes[i]>=POMDPSettings.NODE_SELECTION_THRESHOLD_VALUE]
    # print("***************** Selected Compromised Nodes %s*************************"%(compromised_nodes))
    return compromised_nodes

def normalize_state_probability(state_space):
    non_zero_prob_sum = sum([state.belief for state in state_space if state.belief > 0])
    # print("******** All Non Zero Probabilitites %s *******"%(non_zero_prob))
    # print("******** Before Normalization : All Non Zero Probabilitites %s *******"%(non_zero_prob_sum))
    for state in state_space:
        state.set_belief(state.belief/non_zero_prob_sum)
    non_zero_prob_sum = sum([state.belief for state in state_space if state.belief > 0])
    # print("******** After Normalization : All Non Zero Probabilitites %s *******" % (non_zero_prob_sum))
    if non_zero_prob_sum != 1.0:
        print('************** Sum of probabilities is not One (^_^) (^_^) (^_^) (^_^) %s************'%(non_zero_prob_sum))





