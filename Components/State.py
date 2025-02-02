import POMDPSettings
import math
from CommonUtilities import SetOperations

class State:
    def __init__(self,id,adversary_positions):
        self.primary_key = id
        self.adversary_positions = adversary_positions
        self.state_value = 0.0
        self.belief = 0.0
        self.parent_states = []
        self.current_propagation_probability = [1.0 for i in range(len(adversary_positions))]
        self.number_mirror_node = len([1 for i in adversary_positions if i < 0])
        self.observation_prob = None

    def set_belief(self,prob_value):
        self.belief = prob_value

    def determine_state_value(self):
        # print('***** Adversary Positions ****** %s'%(self.adversary_positions))
        target = POMDPSettings.target_node[0]
        self.state_value = 0.0
        for node in self.adversary_positions:
            if node < 0:
                ######################### It's a honeypot ########################################
                distance_from_target = POMDPSettings.all_pair_shortest_path[target][-node]
                self.state_value += POMDPSettings.GAIN_HONEYPOT + pow(distance_from_target,2)*POMDPSettings.BENEFIT_DISTANCE
                continue

            self.state_value += POMDPSettings.node_values[node]

    def __set_possible_parent_nodes_new(self):
        del self.parent_states[:]
        for node in self.adversary_positions:
            parent_node = POMDPSettings.parent_nodes_considered_paths[node]
            for state in POMDPSettings.state_space:
                if state.primary_key == self.primary_key:
                    continue
                if len(set(parent_node) & set(state.adversary_positions)) > 0:
                    parent_state = True
                    for ref_state_node in state.adversary_positions:
                        if ref_state_node in parent_node or ref_state_node==node:
                            continue
                        if ref_state_node in self.adversary_positions:
                            continue
                        parent_state = False
                        for path_index in POMDPSettings.possible_nodes_for_state:
                            path = POMDPSettings.possible_nodes_for_state[path_index]
                            if ref_state_node in path and node in path:
                                if path.index(node) > path.index(ref_state_node):
                                    parent_state = True
                                    break
                    if parent_state:
                        parent_state_id = POMDPSettings.state_space_map[tuple(state.adversary_positions)]
                        if parent_state_id not in self.parent_states:
                            self.parent_states.append(parent_state_id)


    def set_possible_parent_nodes(self):
        if not POMDPSettings.TAKE_MIRROR_COMPROMISED_NODES:
            self.__set_possible_parent_nodes_new()
            return
        # print('********** Parent Nodes %s ***********' % (POMDPSettings.parent_nodes_considered_paths))
        # print('********** Current Adversary Positions %s ***********'%(self.adversary_positions))
        del self.parent_states[:]
        for node in self.adversary_positions:
            if node < 0:
                node = -node
            parent_node = POMDPSettings.parent_nodes_considered_paths[node]
            for state in POMDPSettings.state_space:
                if state.primary_key == self.primary_key:
                    continue
                if len(set(parent_node) & set(state.adversary_positions)) > 0:
                    mirror_node_exists = False
                    for node_parent in state.adversary_positions:
                        if -node_parent in self.adversary_positions:
                            mirror_node_exists = True
                            break
                    if not mirror_node_exists:
                        ############## Check if the considered node is the only difference node from the old state ####################
                        difference_exists = False
                        union_of_nodes = set(self.adversary_positions) | set(state.adversary_positions)
                        for check_if_difference_node in union_of_nodes:
                            if check_if_difference_node == node or check_if_difference_node == -node:
                                continue
                            if check_if_difference_node in parent_node:
                                continue
                            if check_if_difference_node not in state.adversary_positions or\
                                    check_if_difference_node not in self.adversary_positions:
                                difference_exists = True
                                break
                        if not difference_exists:
                            self.parent_states.append(POMDPSettings.state_space_map[tuple(state.adversary_positions)])

    def get_observation_probability(self):
        if self.observation_prob is None:
            self.observation_prob = [1.0 for i in range(2)]
            for node in self.adversary_positions:
                if node >= 0:
                    self.observation_prob[0] *= POMDPSettings.IDS_TRUE_POSITIVE_RATE
                    self.observation_prob[1] *= POMDPSettings.IDS_FALSE_POSITIVE
                else:
                    self.observation_prob[0] *= POMDPSettings.MIRROR_NODE_TRUE_POSITIVE
                    self.observation_prob[1] *= POMDPSettings.MIRROR_NODE_FALSE_POSITIVE
        return self.observation_prob

    def print_properties(self,parent_print=False):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Adversary Positions :%s"%(self.adversary_positions))
        print('\t Possible Parent States : %s' % (self.parent_states))
        if parent_print:
            for each_state in self.parent_states:
                print('\t \t States %s : %s'%(each_state,POMDPSettings.state_space[each_state].adversary_positions))
        print("\t State Value :%s"%(self.state_value))
        print("\t State Belief :%s" % (self.belief))
        print('\t Current Propagation probability from pervious state %s'%(self.current_propagation_probability))
        print('\t Number of Mirror Nodes in the state %s'%(self.number_mirror_node))