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

