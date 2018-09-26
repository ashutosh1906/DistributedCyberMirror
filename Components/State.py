class State:
    def __init__(self,id,adversary_positions):
        self.primary_key = id
        self.adversary_positions = adversary_positions
        self.state_value = 0.0
        self.belief = 0.0

    def set_belief(self,prob_value):
        self.belief = prob_value

    def print_properties(self):
        print("\t ------> Primary Key %s"%(self.primary_key))
        print("\t Adversary Positions :%s"%(self.adversary_positions))
        print("\t State Value :%s"%(self.state_value))
        print("\t State Belief :%s" % (self.belief))