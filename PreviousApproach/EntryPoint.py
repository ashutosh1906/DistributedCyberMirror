from PreviousApproach import POMDPSettings
from PreviousApproach import Utilities
import Dijkstra
from Components import State
from PreviousApproach import POMDPModules

def create_state_space():
    primary_id = 1
    for state_id in POMDPSettings.state_list:
        state_full_name = state_id
        state_short_name = POMDPSettings.state_list[state_full_name][0]
        state_value = POMDPSettings.state_list[state_full_name][1]
        POMDPSettings.State_space.append(State.State(primary_id,state_full_name,state_short_name,state_value))
        primary_id = primary_id << 1

def initialization():
    create_state_space()
    # Utilities.print_space_properties() ################ Print Space Properties
    ParseTopologyFile.parse_aSHIIP_topology(POMDPSettings.TOPOLOGY_FILE_NAME, POMDPSettings.adjacent_matrix)
    # Utilities.print_Topology(POMDPSettings.adjacent_matrix)
    ###################### What is the target node and find distance matrix of these nodes to other nodes #############################
    while(True):
        print("Please enter the target node. Any number between [0-%s]"%(len(POMDPSettings.adjacent_matrix)-1))
        user_input_target_node = int(input())
        if user_input_target_node > len(POMDPSettings.adjacent_matrix)-1:
            print("No Such Node. Please try again")
            continue
        POMDPSettings.target_node.append(user_input_target_node) ########### Assuming one target node currently, so index will be 0
        break
    print("Target Node : %s"%(POMDPSettings.target_node))
    Utilities.generate_inital_probability()
    print("Initial Belief %s"%(POMDPSettings.initial_belief_position))
    POMDPSettings.all_pair_shortest_path[POMDPSettings.target_node[0]] = \
        Dijkstra.Dijkstra_algorithm_unweighted(POMDPSettings.target_node[0],POMDPSettings.adjacent_matrix)
    POMDPModules.generate_initial_state()

if __name__=='__main__':
    print("Start of the CyberMIRROR Model")
    initialization()
    while(True):
        print("Enter the Commands:\n"
              "---> Press %s for Running\n"
              "---> Press %s to Exit"%(POMDPSettings.RUN_PROGRAM,POMDPSettings.END_PROGRAM))
        run_status = int(input())
        if run_status==POMDPSettings.END_PROGRAM:
            print('***************** Terminating the Program *********************')
            break