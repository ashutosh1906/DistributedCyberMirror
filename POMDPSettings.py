import math
##################################### File Location System #####################
INPUT_FILES_DIRECTORY = 'InputFiles'
CONFIGURATION_FILES_DIRECTORY = 'ConfigurationFiles'

####################################### Topology #####################################
TOPOLOGY_FILE_NAME = '%s/Topology/Topology1.txt'%(INPUT_FILES_DIRECTORY)
adjacent_matrix = []
all_pair_shortest_path = {}

#################################### Configurations ###################################
ADVERSARY_LOGS = '%s/adv_initial_position'%(CONFIGURATION_FILES_DIRECTORY)
READ_IMPACT_FROM_FILE = True

###################################### Environment ###################################
impact_nodes = {}
compromised_nodes_probability = {}
target_node = [] ############### Targets can be a list of probable targets #########################
                 ############### if only one target access with the index 0#######################

#################################### SELECTING COMPROMISED NODES ##################################
COMPROMISED_NODES_SELECTION_ON_THRESHOLD = True
NODE_SELECTION_THRESHOLD_VALUE = 300
compromised_nodes_current_time = []
MAXIMUM_DEPTH_CHECK = True

############################################# POMDP Components ####################################
DISCOUNT_FACTOR = 0.6
MAXIMUM_DEPTH = int(math.log(0.01)/math.log(DISCOUNT_FACTOR)+1) ###### (Dis. Fact)^n >= 0.01
                                                         ###### n is the meximum depth
state_space = []
state_space_map = {}

################################## Other Variables ##################################################
READ_IDS_FROM_FILES = True
USER_INPUT_TARGET_NODE = False
STATIC_TARGET_NODE = [3]