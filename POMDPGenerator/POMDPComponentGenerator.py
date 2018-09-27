from Components import State
import POMDPSettings
from CommonUtilities import SetOperations

def generate_initial_state_space(possible_nodes_for_state):
    print('**** Possible Initial Adversary Positions %s'%(possible_nodes_for_state))
    compromised_hosts_by_position = list(possible_nodes_for_state.keys())
    taken_node = {}
    adv_position_node = []
    for i in range(len(compromised_hosts_by_position)):
        adv_position_node.append([])
        for node in possible_nodes_for_state[compromised_hosts_by_position[i]]:
            adv_position_node[i].append(node)
            adv_position_node[i].append(-node)
    print("Adversary Position Nodes %s"%(adv_position_node))
    iterate_over_possible_state(adv_position_node,1,len(compromised_hosts_by_position),[])

def iterate_over_possible_state(adv_position_node,current_depth,max_depth,chosen_node):
    # print('Current Depth %s Chosen Nodes %s'%(current_depth,chosen_node))
    if current_depth > max_depth:
        return
    if current_depth==max_depth:
        state_id = len(POMDPSettings.state_space)
        for node in adv_position_node[current_depth-1]:
            current_state = []
            for i in chosen_node:
                current_state.append(i)
            current_state.append(node)
            POMDPSettings.state_space.append(State.State(state_id,current_state))
            POMDPSettings.state_space_map[tuple(current_state)] = state_id
            state_id += 1
            # print("\t Current State is %s"%(current_state))
        return
    for node in adv_position_node[current_depth-1]:
        current_state = []
        for i in chosen_node:
            current_state.append(i)
        current_state.append(node)
        iterate_over_possible_state(adv_position_node,current_depth+1,max_depth,current_state)

def iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,current_depth,
                                 chosen_node,state_space,state_space_map):
    if current_depth > len(compromised_nodes_current_time):
        # print('*** Assign and Update Belief of the States %s :: %s'%(chosen_node,state_space_map[tuple(chosen_node)]))
        prob = 1.0
        for node in chosen_node:
            if node in compromised_nodes_probability:
                prob *= compromised_nodes_probability[node]
            if -node in compromised_nodes_probability:
                prob *= (1-compromised_nodes_probability[-node])
        state_id = state_space_map[tuple(chosen_node)]
        # print(
        #     '*** Assign and Update Belief of the States %s :: %s --> %s' % (chosen_node,state_id,prob))
        state_space[state_id].set_belief(prob)
        return
    first_adv_position = compromised_nodes_current_time[current_depth-1]
    chosen_node.append(first_adv_position)
    iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,
                                 current_depth+1,chosen_node,state_space,state_space_map)
    del chosen_node[-1]
    chosen_node.append(-first_adv_position)
    iterate_over_possible_belief(compromised_nodes_current_time, compromised_nodes_probability,
                                current_depth + 1,
                                chosen_node,state_space,state_space_map)
    del chosen_node[-1]

def generate_initial_belief(compromised_nodes_current_time,compromised_nodes_probability,state_space,state_space_map):
    print('***** Selectected Compromised Nodes %s'%(compromised_nodes_current_time))
    print('***** Selectected Compromised Nodes Prob %s' % (compromised_nodes_probability))
    print('******* State Space ************** %s'%(len(state_space)))
    print('******* State Space Map ************** %s' % (state_space_map))
    iterate_over_possible_belief(compromised_nodes_current_time,compromised_nodes_probability,
                                 1,[],state_space,state_space_map)


def initialize_action_space():
    index = 0
    del POMDPSettings.action_space_by_type[:]
    if POMDPSettings.SPATIAL_MUTATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.SPATIAL_MUTATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.spatial_mutation)
        index += 1

    if POMDPSettings.TEMPORAL_MUTATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.TEMPORAL_MUTATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.temporal_mutation)
        index += 1

    if POMDPSettings.DIVERSITY_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.DIVERSITY_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.diversity)
        index += 1

    if POMDPSettings.ANONYMIZATION_ENABLED:
        POMDPSettings.action_space_group_index[index] = POMDPSettings.ANONYMIZATION_INDEX
        POMDPSettings.action_space_by_type.append(POMDPSettings.anonymization)
        index += 1

    SetOperations.combination_possible_values_all_positions(POMDPSettings.action_space_by_type)








