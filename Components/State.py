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

    def set_possible_parent_nodes(self):
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
                        for check_if_difference_node in self.adversary_positions:
                            if check_if_difference_node == node or check_if_difference_node == -node:
                                continue
                            if check_if_difference_node not in state.adversary_positions:
                                difference_exists = True
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