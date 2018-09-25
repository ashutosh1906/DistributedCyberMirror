import POMDPSettings
import Dijkstra

def generate_initial_state():
    print("IDS Adbersary Positions %s"%(POMDPSettings.initial_belief_position))
    POMDPSettings.belief_space[0] = [0.0 for i in range(len(POMDPSettings.State_space))]
    for adv_position in POMDPSettings.initial_belief_position:
        min_distance = Dijkstra.Dijkstra_algorithm_unweighted_pair\
            (POMDPSettings.target_node[0],adv_position,POMDPSettings.adjacent_matrix)
        # print("Min Distance of %s from %s is %s"%(POMDPSettings.target_node[0],adv_position,min_distance))
        index_adv = POMDPSettings.LOW_PROXIMITTY_INDEX ###################### Low Proximity
        if adv_position==POMDPSettings.target_node[0]:
            index_adv = POMDPSettings.COMPROMISED_INDEX
        elif adv_position in POMDPSettings.current_honeypot:
            index_adv = POMDPSettings.HONEYPOT_INDEX
        if min_distance > POMDPSettings.LOW_PROXIMITY_DISTANCE:
            if min_distance < POMDPSettings.HIGH_PROXIMITY_DISTANCE:
                index_adv = POMDPSettings.MEDIUM_PROXIMITTY_INDEX
            else:
                index_adv = POMDPSettings.HIGH_PROXIMITTY_INDEX
        POMDPSettings.belief_space[0][index_adv] += POMDPSettings.initial_belief_position[adv_position]

    if sum(POMDPSettings.belief_space[0]) != 1.0:
        ############################ Normalization to be aggregated into 1.0#########################
        for index in range(len(POMDPSettings.belief_space[0])):
            POMDPSettings.belief_space[0][index] /= sum(POMDPSettings.belief_space[0])
    print("Initial Belief State %s Total %s" % (POMDPSettings.belief_space[0], sum(POMDPSettings.belief_space[0])))
