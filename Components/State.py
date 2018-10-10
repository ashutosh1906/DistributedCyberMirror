import POMDPSettings
import math
from CommonUtilities import SetOperations

class State:
    def __init__(self,id,adversary_positions):
        self.primary_key = id
        self.adversary_positions = adversary_positions
        self.state_value = 0.0
        self.belief = 0.0
        self.parent_nodes = []
        self.__determine_state_value()
        self.__set_possible_parent_nodes()


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

    def __set_possible_parent_nodes(self):
        # print('********** Initial Compromised Nodes %s ***********' % (POMDPSettings.compromised_nodes_current_time))
        # print('********** Possible Adversary Positions %s ***********' % (POMDPSettings.possible_nodes_for_state))
        # print('********** Current Adversary Positions %s ***********'%(self.adversary_positions))
        del self.parent_nodes[:]
        adv_position_index = []
        adv_position_id = 0
        for node in POMDPSettings.compromised_nodes_current_time:
            try:
                adv_position_index.append(POMDPSettings.possible_nodes_for_state[node].
                                          index(self.adversary_positions[adv_position_id]))
            except ValueError:
                adv_position_index.append(POMDPSettings.possible_nodes_for_state[node].
                                          index(-self.adversary_positions[adv_position_id]))
            adv_position_id += 1
        # print('********* Parent Nodes Index %s'%(adv_position_index))
        # print('********** Adversary Position Nodes %s'%(POMDPSettings.adversary_position_nodes))
        number_of_compromised = len(adv_position_index)
        for adv_index in range(number_of_compromised):
            current_adv_node_index = adv_position_index[adv_index]
            if current_adv_node_index <= 0:
                continue
            else:
                parent_node = POMDPSettings.possible_nodes_for_state[POMDPSettings.compromised_nodes_current_time[adv_index]][current_adv_node_index-1]
            data_structure = []
            for i in range(0,adv_index):
                data_structure.append(POMDPSettings.adversary_position_nodes[i])
            data_structure.append([parent_node])
            for i in range(adv_index+1,number_of_compromised):
                data_structure.append(POMDPSettings.adversary_position_nodes[i])
            possible_combination = SetOperations.combination_possible_values_all_positions(data_structure)
            self.parent_nodes.append(possible_combination)
            # print('\t \t *** Possible Parent Nodes %s'%(possible_combination))

    def print_properties(self):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Adversary Positions :%s"%(self.adversary_positions))
        print('\t Possible Parent Nodes : %s'%(self.parent_nodes))
        print("\t State Value :%s"%(self.state_value))
        print("\t State Belief :%s" % (self.belief))