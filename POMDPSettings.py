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
possible_nodes_for_state = {}
parent_nodes_of_each_node = {}
possible_node_combinations = {}
parent_nodes_considered_paths = {}
node_values = {}
SORT_ADVERSARY_POSITION = True

#################################### SELECTING COMPROMISED NODES ##################################
COMPROMISED_NODES_SELECTION_ON_THRESHOLD = True
NODE_SELECTION_THRESHOLD_VALUE = 250
compromised_nodes_current_time = []
next_adversary_nodes = []
MAXIMUM_DEPTH_CHECK = True

############################################# POMDP Components ####################################
DISCOUNT_FACTOR = 0.6
MAXIMUM_DEPTH = int(math.log(0.01)/math.log(DISCOUNT_FACTOR)+1) ###### (Dis. Fact)^n >= 0.01
                                                         ###### n is the meximum depth
state_space = []
state_space_map = {}

action_space_by_type = []
action_space_group_index = {}
action_space_all_values = []
action_space_objects = []

spatial_mutation = [0.0,0.25,0.5,0.75,1.0]
SPATIAL_MUTATION_ENABLED = True
SPATIAL_MUTATION_INDEX = 0

temporal_mutation = [0,10,20,30]
TEMPORAL_MUTATION_ENABLED = False
TEMPORAL_MUTATION_INDEX = 1

diversity = [1,2,4,6]
DIVERSITY_ENABLED = True
DIVERSITY_INDEX = 2

anonymization = [1,2,4,6]
ANONYMIZATION_ENABLED = True
ANONYMIZATION_INDEX = 3

DEFENSE_ACTION_TOTAL = 0

DEFENSE_DO_NOTHING_ACTION = [1.0,1,1]
############################################ State Value Parameters ###################################
LOSS_COMPROMISED = -1000
GAIN_HONEYPOT = 700
BENEFIT_DISTANCE = 100
DISTANCE_FACTOR = 10
TAKE_MIRROR_COMPROMISED_NODES = True

############################################# Action Effectiveness #######################################
CONCEALABILITY_MEASURE_ENABLED = 1
WEIGHT_CONCEALABILITY_MEASURE = 1

DETECTABILITY_MEASURE = 0
WEIGHT_DETECTABILITY_MEASURE = 1
IDS_TRUE_POSITIVE_RATE = 0.9
ROBUSTNESS_DECEPTION = 0.9

DETERRENCE_MEASURE = 0
WEIGHT_DETERRENCE_MEASURE = 1

############################################## Action COST ##########################################
SPATIAL_MUTATION_COST = 100
SPATIAL_MUTATION_DISTANCE_WEIGHT = 1.5 ###### Not Used Right Now

ANONYMIZATION_COST = 100
DIVERSITY_COST = 100

################################## ACTION SPACE REDUCTION #############################################

MARGINAL_PRUNNING = True
MINIMUM_EFFECTIVENESS_WITH_SCAN = 0.50
MINIMUM_EFFECTIVENESS_WITHOUT_SCAN = 0.70

REDUNDANT_PRUNNING = True
CLUSTER_DIFFERENCE = 0.025
REDUNDANT_CLUSTERING_TOLERANCE_LEVEL = 0.001
REDUNDANT_MAX_ITERATION = 100
Y_AXIS_COST_EFFECTIVENESS = False
TRADE_OFF_BENEFIT_COST = 0.7
MAX_CLUSTER_ITERATION = 5

IRRELEVANT_PRUNNING = True
defense_action_id_to_position = {}
action_based_on_nodes = {}

################################## ADVERSARY PARAMETERS #############################################
ADVERSARY_SCANNING_PROB = 0.50
ADVERSARY_SCANNING_COST = 100

ADVERSARY_ADVANCE = 0.7
ADVERSARY_ADVANCE_COST = 100

ADVERSARY_DO_NOTHING = 1-ADVERSARY_ADVANCE
adversary_action_objects = []
adversary_action_id_to_position = {}

adversary_position_nodes = []

############################# State Transition #####################################################
state_transition_with_adversary = {}
state_transition_to_id = {}


################################## Other Variables ##################################################
READ_IDS_FROM_FILES = True
USER_INPUT_TARGET_NODE = False
STATIC_TARGET_NODE = [3]