import POMDPSettings
import random

def generate_inital_probability(i=0):
    POMDPSettings.initial_belief_position.clear()
    if POMDPSettings.INITIAL_ADVERSARY_READ_FROM_FILE:
        read_adversary_position_file()
    else:
        random_adversary_position()

def normalize_dict(dict):
    total_prob = 0.0
    for key_current in dict.keys():
        total_prob += dict[key_current]
    if total_prob != 1.0:
        normalized_value = 0.0
        for key_current in dict.keys():
            dict[key_current] /= total_prob
            normalized_value += dict[key_current]
        total_prob = normalized_value

    if total_prob != 1.0:
        print("***** (^_^) (^_^) Error in Total Probability %s (^_^) (^_^) ******"%(total_prob))
        # assign_normalization_error(total_prob,dict)

def assign_normalization_error(total_prob,dict):
        for keys in dict.keys():
            value = dict[keys]
            value -= (total_prob-1.0)
            if value < 0.0 or value > 1.0:
                continue
            dict[keys] = value
            break
        current_total_prob = 0.0
        for keys in dict.keys():
            current_total_prob += dict[keys]
        if current_total_prob != 1.0:
            print("***** (*_*) (*_*) Error Correction Didn't Work %s (*_*) (*_*) ******"%(current_total_prob))



def random_adversary_position():
    total_prob = 0.0
    while (True):
        if len(POMDPSettings.initial_belief_position) == POMDPSettings.INITIAL_NUMBER_OF_POSITION:
            break
        while (True):
            node = random.randint(0, len(POMDPSettings.adjacent_matrix) - 1)
            if node in POMDPSettings.initial_belief_position:
                continue
            POMDPSettings.initial_belief_position[node] = random.uniform(0.1, 1.0)
            total_prob += POMDPSettings.initial_belief_position[node]
            break

    if total_prob != 1.0:
        normalize_dict(POMDPSettings.initial_belief_position)

def read_adversary_position_file():
    file_pointer = open('%s/%s'%(POMDPSettings.CONFIGURATION_DIRECTORY,POMDPSettings.ADVERSARY_LOGS),'r+')
    total_prob = 0.0
    for line in file_pointer:
        line = line.replace('\n','').split(',')
        node = int(line[0])
        belief = float(line[1])
        if belief > 0.0:
            POMDPSettings.initial_belief_position[node] = belief
            total_prob += belief
    file_pointer.close()
    # print("Tota Prob --> %s"%(total_prob))
    if total_prob != 1.0:
        normalize_dict(POMDPSettings.initial_belief_position)


def print_Topology(adjacent_matrix):
    print("***************** Topology Information *********************")
    for i in range(len(adjacent_matrix)):
        print("Node ID %s"%(i))
        print("\t Adjacent Nodes %s"%(adjacent_matrix[i]))

def print_space_properties():
    print("************************** State Properties ***************************")
    for state in POMDPSettings.State_space:
        state.print_properties()

