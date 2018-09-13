def print_Topology(adjacent_matrix):
    print("***************** Topology Information *********************")
    for i in range(len(adjacent_matrix)):
        print("Node ID %s"%(i))
        print("\t Adjacent Nodes %s"%(adjacent_matrix[i]))