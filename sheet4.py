### Part 1: Dijkstra's algorithm ###

# The Dijkstra algorithm allows to find the shortest path between any two nodes in a given network. Here we implement the easy version of Dijkstra, where all nodes have the same value: we assume all edges to be equal and that all edges are explicitely present (i.e. A (pp) B and B (pp) A for a symmetric network). 


# Task 1: prepare environment for simplest version of Dijkstra

# In order to compute the shortest paths between a given node and all other nodes in your network we split the problem into several smaller functions. 
    
#  input: fileName = name of file with network information
#  output: net = array with network
#
def load_network(fileName):  # load the network
    f = open(fileName, "r")
    # An edge is given by net[i][1] and the nodes are net[i][0] and net[i][2] 
    net = []
    for line in f:
        line.rstrip('\r\n').split('\t')
        net.append(line.rstrip('\r\n').split('\t'))  
    f.close()
    return net

#  iinput: network = matrix
#  output: nodeS = list of nodes
#
def get_list_nodes(network):	# create a list of nodes 
    nodeS = set()
    for i in range(len(network)):
        #print network[i][0]
        nodeS.add(network[i][0])
    return list(nodeS)

#  input: nodes = list of nodes
#  output: pos = dictionary with position of each node
#
def create_hash_node_idx(nodes):	# create a hash for the list of nodes
    pos = {}
    for i in range(len(nodes)):
        pos[nodes[i]]=i
    return pos

#  input: file_output = array to be searched
#         node = element to be searched in array
#         start = string of starting node
#         pstart = position of starting string
#         number_nodes = number of nodes in network
#
def export_result(file_output,node,start,pstart,number_nodes):
    # Write in the file the shortest path for each node per line
    out = open(file_output, 'w')
    for i in range(number_nodes):
        out.write('{}:\t'.format(node[i]))
        p=i
        while p != pstart:
            out.write('{}-'.format(node[p]))
            p=parent[p]
        out.write('{}\n'.format(start))
    out.close()

#  input: node = element to be searched in array
#         start = string of starting node
#         pstart = position of starting string
#         number_nodes = number of nodes in network
#         parent = list of parent nodes from which node has been reached
#
def print_result(node,start,pstart,number_nodes, parent):    
    #print the shortest path for each node  
    for i in range(number_nodes):
        print ('{}:\t'.format(node[i]),)
        p=i
        while p != pstart:
            print ('{}-'.format(node[p]),)
            p=parent[p]
        print ('{}\n'.format(start)) 
        
        
# Task 2: implement Dijkstra

# input file with network data
# toy.sif: toy network as in the instruction Figure
# network_final_sym.sif: Network of the NBT Primer, with all symmetric edges

fileName="toy.sif"

# Set the node from which all shortest paths will be computed
start='A'

def dijkstra(fileName, start):
     # Load the network
    net = load_network(fileName)
    print (net)
    number_edges = len(net) # number of edges
    nodes = get_list_nodes(net)     # get the list of nodes
    print (nodes)
    number_nodes = len(nodes) # number of nodes
    # Create a hash to link a node with its relted position within the node list
    pos = create_hash_node_idx(nodes)
    # Init the variable for Dijkstra's algorithm
    pstart = pos[start] 
    # Index of the starting node
    Max=100000 
    # Maximal distance to prevent too long computation
    d=0 # distance to the starting node
    # This is the list of parent nodes (from which a node has been reached)
    parent = [0]*number_nodes
    # This is the distance to the starting node
    dist = [Max]*number_nodes 
    # This is the list of nodes that have been monitored
    seen = [] 
    dist[pstart]=d 
    seen.append(pstart)
    while len(seen) < number_nodes: # as long as all nodes have not been visited
        for i in range(number_edges): # for each edge in the network 
            if dist[pos[net[i][0]]]==d and dist[pos[net[i][2]]]==Max: # if node_A is at distance of interest + node_B not yet computed
                dist[pos[net[i][2]]]=d+1 # set to node_B the distance of interest of the next iteration +1 here because vertices not labeled
                parent[pos[net[i][2]]]=pos[net[i][0]] # set node_A as parent of node_B
                seen.append(pos[net[i][2]]) # tag node_B as seen
        d=d+1 # increase the distance to the starting node   
    print_result(nodes,start,pstart,number_nodes,parent)

# write to output
export_result('shortest_path_test.txt',node,start,pstart,number_nodes)

