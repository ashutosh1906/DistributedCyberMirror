import POMDPSettings
import math
class Actions:
    def __init__(self,id,node,action_component):
        self.primary_key = id
        self.node_id = node
        self.distance_from_target = 0
        self.__distance_from_target()
        self.spatial_mutation = None
        self.temporal_mutation = None
        self.diversity = None
        self.anonymization = None
        self.benefit = None
        self.cost = None
        self.weighted_effectiveness = None
        self.weighted_cost_effectiveness = None
        for action_type in range(len(action_component)):
            if POMDPSettings.action_space_group_index[action_type]==POMDPSettings.SPATIAL_MUTATION_INDEX:
                self.spatial_mutation = action_component[action_type]
            if POMDPSettings.action_space_group_index[action_type] == POMDPSettings.TEMPORAL_MUTATION_INDEX:
                self.temporal_mutation = action_component[action_type]
            if POMDPSettings.action_space_group_index[action_type] == POMDPSettings.DIVERSITY_INDEX:
                self.diversity = action_component[action_type]
            if POMDPSettings.action_space_group_index[action_type] == POMDPSettings.ANONYMIZATION_INDEX:
                self.anonymization = action_component[action_type]
        self.effeciveness_with_scan = None
        self.effeciveness_without_scan = None
        self.probable_ancestor_nodes = POMDPSettings.ancestor_nodes_of_each_node[self.node_id]
        self.__setCost()

    def __distance_from_target(self):
        target_node = POMDPSettings.target_node[0]
        if self.node_id==target_node:
            self.distance_from_target = 0
            return
        self.distance_from_target = POMDPSettings.all_pair_shortest_path[target_node][self.node_id]

    def __setCost(self):
        self.cost = 0.0
        if self.anonymization is not None:
            self.cost += (self.anonymization-1)*POMDPSettings.ANONYMIZATION_COST
        if self.diversity is not None:
            self.cost += (self.diversity-1)*POMDPSettings.DIVERSITY_COST
        ########################## Spatial Mutation Number of IP Address ##################
        ####################### t_i = (1-m)*(n-1) ########################################
        if self.spatial_mutation is not None:
            spatial_ip = (1-self.spatial_mutation)*(len(self.probable_ancestor_nodes) - 1)
            if spatial_ip != int(spatial_ip):
                spatial_ip = int(spatial_ip)+1
            self.cost += spatial_ip*POMDPSettings.SPATIAL_MUTATION_COST
        # print('*** Required Cost is %s for Node %s*******'%(self.cost,self.node_id))
        # self.printProperties()

    def printProperties(self):
        print('\n\tAction ID : %s'%(self.primary_key))
        print('\t\t Node ID : %s'%(self.node_id))
        print('\t\t\t <-----> Distance from the target %s'%(self.distance_from_target))
        print('\t\t\t <-----> Probable Parent Nodes %s' % (self.probable_ancestor_nodes))
        if self.spatial_mutation is not None:
            print('\t\t Spatial Mutation : %s'%(self.spatial_mutation))
        if self.temporal_mutation is not None:
            print('\t\t Temporal Mutation : %s'%(self.temporal_mutation))
        if self.diversity is not None:
            print('\t\t Diversity : %s'%(self.diversity))
        if self.anonymization is not None:
            print('\t\t Anonymization : %s'%(self.anonymization))
        print('\t\t Effectiveness with Scan %s'%(self.effeciveness_with_scan))
        print('\t\t Effectiveness "without" Scan %s' % (self.effeciveness_without_scan))
        if self.cost is not None:
            print('\t\t Implementation Cost %s'%(self.cost))
        if self.weighted_effectiveness is not None:
            print('\t\t Weighted Effectiveness %s'%(self.weighted_effectiveness))
        if self.weighted_cost_effectiveness is not None:
            print('\t\t Weighted Cost Effectiveness %s'%(self.weighted_cost_effectiveness))


    def set_effectiveness(self):
        self.effeciveness_with_scan = 0.0
        self.effeciveness_without_scan = 0.0
        prev_anonymity = 0
        prev_diversity = 0
        if self.node_id in POMDPSettings.deployed_defense_nodes:
            if POMDPSettings.ANONYMIZATION_ENABLED:
                prev_anonymity += POMDPSettings.deployed_defense_nodes[self.node_id][POMDPSettings.ANONYMIZATION_INDEX]-1
        #if self.node_id in POMDPSettings.deployed_defense_nodes:
            if POMDPSettings.DIVERSITY_ENABLED:
                prev_diversity += POMDPSettings.deployed_defense_nodes[self.node_id][POMDPSettings.DIVERSITY_INDEX]-1

        effectiveness_anony_diversity = (1-1/((self.anonymization+prev_anonymity)*(self.diversity+prev_diversity)))

        if POMDPSettings.CONCEALABILITY_MEASURE_ENABLED:
            concealability_measure = math.exp(-1)+(1-math.exp(-1))*effectiveness_anony_diversity
            self.effeciveness_with_scan = concealability_measure*POMDPSettings.WEIGHT_CONCEALABILITY_MEASURE
            self.effeciveness_without_scan = (1-(1-concealability_measure)*self.spatial_mutation)*POMDPSettings.WEIGHT_CONCEALABILITY_MEASURE

        if POMDPSettings.DETECTABILITY_MEASURE:
            detectability_measure = effectiveness_anony_diversity*\
                                    POMDPSettings.IDS_TRUE_POSITIVE_RATE*POMDPSettings.ROBUSTNESS_DECEPTION
            self.effeciveness_without_scan += detectability_measure*POMDPSettings.WEIGHT_DETECTABILITY_MEASURE
            self.effeciveness_with_scan += detectability_measure*POMDPSettings.WEIGHT_DETECTABILITY_MEASURE

        if POMDPSettings.DETERRENCE_MEASURE:
            pass
        self.__error_check()

    def __error_check(self):
        if self.effeciveness_with_scan > 1:
            print('##### E R R O R : Error in effectiveness with scan %s \n\t\t Action ID : %s'%(self.effeciveness_with_scan,self.primary_key))
        if self.effeciveness_without_scan > 1:
            print('##### E R R O R : Error in effectiveness without scan %s \n\t\t Action ID : %s'%(self.effeciveness_without_scan,self.primary_key))

    def set_weighted_effectiveness(self,effectiveness):
        self.weighted_effectiveness = effectiveness

    def set_weighted_cost_effectiveness(self,cost_effectiveness):
        self.weighted_cost_effectiveness = cost_effectiveness


