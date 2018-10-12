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
        self.__determine_state_value()

    def set_belief(self,prob_value):
        self.belief = prob_value

    def __determine_state_value(self):
        # print('***** Adversary Positions ****** %s'%(self.adversary_positions))
        target = POMDPSettings.target_node[0]
        self.state_value = 0.0
        for node in self.adversary_positions:
            if node < 0:
                ######################### It's a honeypot ########################################
                distance_from_target = POMDPSettings.all_pair_shortest_path[target][-node]
                self.state_value += POMDPSettings.GAIN_HONEYPOT + distance_from_target*POMDPSettings.BENEFIT_DISTANCE
                continue

            distance_from_target = POMDPSettings.all_pair_shortest_path[target][node]
            self.state_value += POMDPSettings.LOSS_COMPROMISED/math.pow(POMDPSettings.DISTANCE_FACTOR,distance_from_target)

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
                    self.parent_states.append(POMDPSettings.state_space_map[tuple(state.adversary_positions)])

    def print_properties(self,parent_print=False):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Adversary Positions :%s"%(self.adversary_positions))
        print('\t Possible Parent States : %s' % (self.parent_states))
        if parent_print:
            for each_state in self.parent_states:
                print('\t \t States %s : %s'%(each_state,POMDPSettings.state_space[each_state].adversary_positions))
        print("\t State Value :%s"%(self.state_value))
        print("\t State Belief :%s" % (self.belief))