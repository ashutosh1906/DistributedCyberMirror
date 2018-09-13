import ParseTopologyFile,POMDPSettings
import Utilities
import Dijkstra

def initialization():
    ParseTopologyFile.parse_aSHIIP_topology(POMDPSettings.TOPOLOGY_FILE_NAME, POMDPSettings.adjacent_matrix)
    # Utilities.print_Topology(POMDPSettings.adjacent_matrix)
    for i in range(10):
        POMDPSettings.all_pair_shortest_path[i]=Dijkstra.Dijkstra_algorithm_unweighted(i, POMDPSettings.adjacent_matrix)


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