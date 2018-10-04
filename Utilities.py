import POMDPSettings
import random
from CommonUtilities import DataStructureFunctions

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

def reachable_from_other_nodes():
    POMDPSettings.parent_nodes_of_each_node.clear()
    # print("Possible Nodes for State %s"%(POMDPSettings.possible_nodes_for_state))
    for initial_compromised in POMDPSettings.possible_nodes_for_state:
        for node in POMDPSettings.possible_nodes_for_state[initial_compromised]:
            if  node not in POMDPSettings.parent_nodes_of_each_node:
                POMDPSettings.parent_nodes_of_each_node[node] = []
            try:
                node_position = POMDPSettings.possible_nodes_for_state[initial_compromised].index(node)
                for cand_node in POMDPSettings.possible_nodes_for_state[initial_compromised][0:node_position]:
                    if cand_node not in POMDPSettings.parent_nodes_of_each_node[node]:
                        POMDPSettings.parent_nodes_of_each_node[node].append(cand_node)
            except ValueError:
                continue


#################################### Temporary Modules ########################################################################
###################################################### Clustering Algorithms ######################################
def create_clusters(weighted_effectiveness_action,weighted_cost_effectiveness_action,number_of_cluster):
    DataStructureFunctions.normalization_by_min(weighted_effectiveness_action)
    DataStructureFunctions.normalization_by_min(weighted_cost_effectiveness_action)
    number_of_elements = len(weighted_effectiveness_action)
    # print(weighted_effectiveness_action)
    # print(weighted_cost_effectiveness_action)
    # print('Number of cluster %s for %s elements'%(number_of_cluster,number_of_elements))

    ######################################### Pick 10 Random Poinrts for clustering #################################
    centroid_list = []
    mean_cluster = []
    number_taken = 0
    while(True):
        random_num = random.randint(0,number_of_elements-1) ################# Return a random integer N such that a <= N <= b. ##################
        if random_num in centroid_list:
            continue
        centroid_list.append(random_num)
        mean_cluster.append([weighted_effectiveness_action[random_num],weighted_cost_effectiveness_action[random_num]])
        number_taken += 1
        if number_taken==number_of_cluster:
            break
    # print("mean cluster %s"%(mean_cluster))

    difference_between_two_iteration = 1
    iteration_index = 0
    cluster_index = [0 for i in range(number_of_elements)]
    distance_current_iteration = 0
    distance_previous_iteration = 0
    best_k_mean_cluster = None
    best_mean_cluster = None
    while difference_between_two_iteration > POMDPSettings.REDUNDANT_CLUSTERING_TOLERANCE_LEVEL:
        k_means_cluster = [[] for i in range(number_of_cluster)]
        for element_index in range(number_of_elements):
            min_distance = -1
            cluster_id = 0
            for centroid in mean_cluster:
                current_distance = pow((weighted_effectiveness_action[element_index]-centroid[0]),2)\
                                   +pow((weighted_cost_effectiveness_action[element_index]-centroid[1]),2)
                current_distance = pow(current_distance,0.5) #### Sqrt #######
                # print("Distance from Cluster %s is %s"%(cluster_id,current_distance))
                if min_distance == -1:
                    min_distance = current_distance
                    cluster_index[element_index] = cluster_id
                else:
                    if min_distance > current_distance:
                        min_distance = current_distance
                        cluster_index[element_index] = cluster_id
                cluster_id += 1
            k_means_cluster[cluster_index[element_index]].append(element_index)
            # print("Selected Cluster %s"%(cluster_index[element_index]))
        ############################ Calculate the mean of the centroid again ##############################
        calculate_mean_cluster(k_means_cluster, weighted_effectiveness_action, weighted_cost_effectiveness_action,
                               mean_cluster)
        # for j in range(len(k_means_cluster)):
        #     print('Cluster %s --> %s'%(j,k_means_cluster[j]))
        if iteration_index==0:
            iteration_index += 1
            distance_current_iteration = error_distance(mean_cluster, k_means_cluster,
                                                        weighted_effectiveness_action,
                                                        weighted_cost_effectiveness_action)
            best_k_mean_cluster = k_means_cluster
            best_mean_cluster = mean_cluster
        else:
            ##################### Calculate the distance ######################################################
            distance_previous_iteration = distance_current_iteration
            distance_current_iteration = error_distance(mean_cluster,k_means_cluster,
                                                        weighted_effectiveness_action,weighted_cost_effectiveness_action)
            difference_between_two_iteration = distance_previous_iteration-distance_current_iteration
            if difference_between_two_iteration > 0:
                best_k_mean_cluster = k_means_cluster
                best_mean_cluster = mean_cluster
            # print("Difference between two iteration %s"%(difference_between_two_iteration))
            iteration_index += 1
        # print("Clustering : Current Iteration Distance %s"%(distance_current_iteration))
        if iteration_index == POMDPSettings.REDUNDANT_MAX_ITERATION:
            break
    distance = error_distance(best_mean_cluster,best_k_mean_cluster,
                                                        weighted_effectiveness_action,weighted_cost_effectiveness_action)
    best_action = trade_off_based_best_action_from_cluster(best_k_mean_cluster,best_mean_cluster,
                                        weighted_effectiveness_action,weighted_cost_effectiveness_action)
    # print(distance)
    DataStructureFunctions.delete_element_with_specific_value(best_action,-1)
    return best_action,distance


def select_the_best_action_from_cluster(k_means_cluster,mean_cluster,
                                        weighted_effectiveness_action,weighted_cost_effectiveness_action):
    best_action = [-1 for i in range(len(mean_cluster))]
    # print(len(k_means_cluster))
    for i in range(len(k_means_cluster)):
        min_distance = -1
        # print('%s:length is %s'%(k_means_cluster[i],len(k_means_cluster[i])))
        for element in k_means_cluster[i]:
            current_distance = pow((weighted_effectiveness_action[element] - mean_cluster[i][0]), 2) \
                               + pow((weighted_cost_effectiveness_action[element] - mean_cluster[i][1]), 2)
            current_distance = pow(current_distance, 0.5)  #### Sqrt #######
            if min_distance == -1:
                min_distance = current_distance
                best_action[i] = element
                # print(best_action)
            else:
                if min_distance > current_distance:
                    min_distance = current_distance
                    best_action[i] = element

    return best_action

def trade_off_based_best_action_from_cluster(k_means_cluster,mean_cluster,
                                        weighted_effectiveness_action,weighted_cost_effectiveness_action):
    best_action = [-1 for i in range(len(k_means_cluster))]
    # print(len(k_means_cluster))
    for i in range(len(k_means_cluster)):
        max_benefit = -1
        # print('%s:length is %s'%(k_means_cluster[i],len(k_means_cluster[i])))
        for element in k_means_cluster[i]:
            benefit = weighted_effectiveness_action[element]*POMDPSettings.TRADE_OFF_BENEFIT_COST
            benefit += weighted_cost_effectiveness_action[element]*(1-POMDPSettings.TRADE_OFF_BENEFIT_COST)
            if max_benefit < benefit:
                max_benefit = benefit
                best_action[i] = element
    return best_action


def calculate_mean_cluster(k_means_cluster,weighted_effectiveness_action,weighted_cost_effectiveness_action,mean_cluster):
    delete_cluster = []
    for i in range(len(mean_cluster)):
        if len(k_means_cluster[i])==0:
            delete_cluster.append(i)
            continue
        mean_cluster[i][0] = sum([weighted_effectiveness_action[element] for element in k_means_cluster[i]])/len(mean_cluster[i])
        mean_cluster[i][1] = sum([weighted_cost_effectiveness_action[element] for element in k_means_cluster[i]])/len(mean_cluster[i])
    DataStructureFunctions.delete_values_by_index_from_list(mean_cluster,delete_cluster)
    DataStructureFunctions.delete_values_by_index_from_list(k_means_cluster,delete_cluster)
    # for j in range(len(mean_cluster)):
    #     print('Mean %s --> %s'%(j,mean_cluster[j]))

def error_distance(mean_cluster,k_means_cluster,weighted_effectiveness_action,weighted_cost_effectiveness_action):
    distance = 0.0
    for i in range(len(mean_cluster)):
        for element in k_means_cluster[i]:
            current_distance = pow((weighted_effectiveness_action[element] - mean_cluster[i][0]), 2) \
                               + pow((weighted_cost_effectiveness_action[element] - mean_cluster[i][1]), 2)
            current_distance = pow(current_distance, 0.5)  #### Sqrt #######
            distance += current_distance
    return distance







