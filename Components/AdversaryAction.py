import POMDPSettings
class Adversary_Action:
    def __init__(self,id,scan,forward,prob,position):
        self.primary_key = id
        self.perform_scan = scan
        self.forward = forward
        self.attack_probability = prob
        self.adv_cost = self.perform_scan*POMDPSettings.ADVERSARY_SCANNING_COST\
                        +self.forward*POMDPSettings.ADVERSARY_ADVANCE_COST
        self.adversary_position = position

    def printProperties(self):
        print('Adversary Action ID %s'%(self.primary_key))
        if self.perform_scan:
            print('\t Scanning is True')
        if self.forward:
            print('\t The adversary will forward')
        print('\t Possibility of the action %s'%(self.attack_probability))
        print('\t Cost of the action %s'%(self.adv_cost))