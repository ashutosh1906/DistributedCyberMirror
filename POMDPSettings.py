############################################## System Environment ###################################
RUN_PROGRAM = 1
END_PROGRAM = 0
TIME_TO_REMEMBER = 2
LOW_PROXIMITY_DISTANCE = 2
HIGH_PROXIMITY_DISTANCE = 4
STEPS_BETWEEN_PHASE = 2

############################################### Topology Information ################################
TOPOLOGY_FILE_NAME = 'Topology/Topology1.txt'
adjacent_matrix = []
all_pair_shortest_path = {}
target_node = []

############################################## POMDP Components #####################################
State_space = []
belief_space = [[] for i in range(TIME_TO_REMEMBER)]
current_honeypot = [6,9]

############################################## Initial Belief Configurations ########################
INITIAL_ADVERSARY_READ_FROM_FILE = True
initial_belief_position = {}
INITIAL_NUMBER_OF_POSITION = 10

############################################ Configurations ########################################
CONFIGURATION_DIRECTORY = 'ConfigurationFiles'
ADVERSARY_LOGS = 'adv_initial_position'

############################################## States ###############################################
state_list = {'Low Proximity':('L',-50),'Medium Proximity':('M',-10),'High Proximity':('H',50),
              'Honeypot':('P',200),'Compromised':('C',-200)}
LOW_PROXIMITTY_INDEX = 0
MEDIUM_PROXIMITTY_INDEX = 1
HIGH_PROXIMITTY_INDEX = 2
HONEYPOT_INDEX = 3
COMPROMISED_INDEX = 4
