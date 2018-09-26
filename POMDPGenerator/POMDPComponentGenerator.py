from Components import State
import POMDPSettings

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
            POMDPSettings.state_space_map[current_state] = state_id
            state_id += 1
            # print("\t Current State is %s"%(current_state))
        return
    for node in adv_position_node[current_depth-1]:
        current_state = []
        for i in chosen_node:
            current_state.append(i)
        current_state.append(node)
        iterate_over_possible_state(adv_position_node,current_depth+1,max_depth,current_state)

def generate_initial_belief():
    pass



