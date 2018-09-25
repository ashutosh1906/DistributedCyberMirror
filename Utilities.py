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
    for node in compromised_nodes_probability:
        if node in all_pair_shortest_path[POMDPSettings.target_node[0]]:
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
        file_pointer.close()


