import math
##################################### File Location System #####################
INPUT_FILES_DIRECTORY = 'InputFiles'
CONFIGURATION_FILES_DIRECTORY = 'ConfigurationFiles'

####################################### Topology #####################################
TOPOLOGY_FILE_NAME = '%s/Topology/Topology21.txt'%(INPUT_FILES_DIRECTORY)
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
ancestor_nodes_of_each_node = {}
possible_node_combinations = {}
parent_nodes_considered_paths = {}
node_values = {}
SORT_ADVERSARY_POSITION = True

#################################### SELECTING COMPROMISED NODES ##################################
COMPROMISED_NODES_SELECTION_ON_THRESHOLD = True
NODE_SELECTION_THRESHOLD_VALUE = 0.0
compromised_nodes_current_time = []
next_adversary_nodes = []
MAXIMUM_DEPTH_CHECK = True

############################################# POMDP Components ####################################
MINIMUM_FUTURE_WEIGHT = .01
DISCOUNT_FACTOR = 0.6
# MAXIMUM_DEPTH = int(math.log(0.01)/math.log(DISCOUNT_FACTOR)+1) ###### (Dis. Fact)^n >= 0.01
                                                         ###### n is the meximum depth
MAXIMUM_DEPTH = 8
MAX_STEPS_TOPOLOGY = 0

current_belief = {}
state_space = []
state_space_map = {}

action_space_by_type = []
action_space_group_index = {}
action_space_all_values = []
action_space_objects = []

spatial_mutation = [0.0,0.25,0.5,0.75,1.0]
SPATIAL_MUTATION_ENABLED = True
SPATIAL_MUTATION_INDEX = 0
MAX_AVAILABLE_IP_ADDRESS = 20

temporal_mutation = [0,10,20,30]
TEMPORAL_MUTATION_ENABLED = False
TEMPORAL_MUTATION_INDEX = 1

diversity = [1,2,4,6]
DIVERSITY_ENABLED = True
DIVERSITY_INDEX = 2

anonymization = [1,2,4,6]
ANONYMIZATION_ENABLED = True
ANONYMIZATION_INDEX = 3
MAX_AVAILABLE_ANONYMITY = 20

DEFENSE_ACTION_TOTAL = 0

DEFENSE_DO_NOTHING_ACTION = [1.0,1,1]
############################################ State Value Parameters ###################################
LOSS_COMPROMISED = -100000
GAIN_HONEYPOT = 700
BENEFIT_DISTANCE = 100
DISTANCE_FACTOR = 10
TAKE_MIRROR_COMPROMISED_NODES = False

############################################# Action Effectiveness #######################################
CONCEALABILITY_MEASURE_ENABLED = 1
WEIGHT_CONCEALABILITY_MEASURE = 1

DETECTABILITY_MEASURE = 0
WEIGHT_DETECTABILITY_MEASURE = 1
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
MINIMUM_EFFECTIVENESS_WITH_SCAN = 0.55
MINIMUM_EFFECTIVENESS_WITHOUT_SCAN = 0.75

REDUNDANT_PRUNNING = True
CLUSTER_DIFFERENCE = 0.03
REDUNDANT_CLUSTERING_TOLERANCE_LEVEL = 0.001
REDUNDANT_MAX_ITERATION = 100
Y_AXIS_COST_EFFECTIVENESS = False
TRADE_OFF_BENEFIT_COST = 0.7
MAX_CLUSTER_ITERATION = 2
THREE_DIMENSIONAL_CLUSTER = True

IRRELEVANT_PRUNNING = True
IRRELEVANT_PRUNNING_THRESHOLD = 0
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
ONE_ADVERSARY_UNIFORM_MOVEMENT = True # If there are three nodes to forward, the probability of forwarding to each node is uniformly distributed.
adversary_state_to_state_probability = {}

############################# State Transition #####################################################
state_transition_with_adversary = {}
state_transition_to_id = {}

state_transition_pomdp = {}

################################### Observations Probability ##################################

IDS_TRUE_POSITIVE_RATE = 0.93
IDS_FALSE_POSITIVE = 0.05
MIRROR_NODE_TRUE_POSITIVE = 0.96
MIRROR_NODE_FALSE_POSITIVE = 0.05
observation_probability = {}
WILDCARD_SYMBOL = 'wWw'
OBSERVATION_ACTION_IRRESPECTIVE = True
PENALTY_WRONG_OBSERVATION = False

############################### Rewards #############################################################
rewards_pomdp = {}

################################ POMDP MODEL FILE##################################
DIR_NAME = 'CyberMirrorPOMDPModels'
POMDP_MODEL_FILE_NAME = 'CyberMirror_5'
POMDP_PRECISION = 1
REGRET_PERCENTAGE = 0.00002

POLICY_FILE_GENERATED = 'InputFiles/Policies/'

################################## Other Variables ##################################################
READ_IDS_FROM_FILES = False
USER_INPUT_TARGET_NODE = False
STATIC_TARGET_NODE = [3]

################################ Parse Policy #########################
pomdp_policy_action_index = []

############################ Final Output ###########################
deployed_defense_nodes = {}
deployed_defense_assessment = {}
OUT_DIR_CONCEAL = 'ConcealConf'
OUT_DEFENSE_PLAN_FILE = 'defense_configuration'
POMDP_POLICY_FILE_NAME = '%s/mirror_automated.policy'%(POLICY_FILE_GENERATED)
ZMDP_EXECUTOR = '../../zmdp/bin/linux3/zmdp'
EVALUATION_PROCESS = True
POMDP_FILE_FAST_PARSING = False
POMDP_TIME_LIMIT_FLAG = False
POMDP_TIME_LIMIT = 60 #IN SECONDS
POMDP_HSVI_SEARCH_STRATEGY = False

######### Evaluation Variables ####################
ADVERSARY_POSITION_FILE_NAME = '%s/adv_position_1'%(CONFIGURATION_FILES_DIRECTORY)
ADVERSARY_PROGRESSION_FROM_FILE_FLAG = True
attack_progression_path = []