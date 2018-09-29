import POMDPSettings
import math

class State:
    def __init__(self,id,adversary_positions):
        self.primary_key = id
        self.adversary_positions = adversary_positions
        self.state_value = 0.0
        self.belief = 0.0
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

    def print_properties(self):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Adversary Positions :%s"%(self.adversary_positions))
        print("\t State Value :%s"%(self.state_value))
        print("\t State Belief :%s" % (self.belief))