"""
created by: Meguenni khalil
meguennikhalil@gmail.com
"""

from heapq import heappush, heappop
import networkx as nx
import matplotlib.pyplot as plt

# creating the network:
# we create a dictionary of nodes with their corresponding coordinates {Node: (x, y)}
positions = {0: (0, 0), 1: (0, 3),
        2: (1, 0), 3: (3, 1), 
        4: (2, 4), 5: (5, 3)} 

# here we configure the neighborhood of each node

# here we configure the neighborhood of each node
# (Node 1, Node 2) <=> Node 1 is a neighbor of Node 2, means that there is an arc between them.
 
neighborhood = [(0, 1), (0, 2), (0, 5), (1, 2), (1, 5), (1, 3), (2, 3), (4, 5)]

"""
Euclidian function is used to calculate the distance between two nodes.
the parameters of the function are the position (x, y) of two nodes.
"""
def distanceEuclid(a, b): 
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

# A* Algorithm 
def A_star(source_node, end_node):
    
    if source_node not in positions or end_node not in positions:
        print("ends not found!")
        return False
    
    close_set = set() # a set that will contain the exploited nodes.
    came_from = {} # used to hold the minimal (optimal) path.
    
    # gscore contain the wheight (distance) of the path that links the source node to the cuurent node
    # for the source node, gscore = 0
    gscore = {positions[source_node]:0} 

    """
    fscore is used by A* algorithm to find the optimal path (minimal fscore is taken)
    it stors the current optimal path + the distance between the current node and the end node (heuristic).
    """    
    fscore = {positions[source_node]:distanceEuclid(positions[source_node], positions[end_node])}
    Heap_nodes = [] # this heap will contain the neighbors of the current node (nearby order).
    heappush(Heap_nodes, (fscore[positions[source_node]], positions[source_node])) # adding the source node, it belongs to the optimal path 
   
    while Heap_nodes: # heap is not empthy
        
        current_node = heappop(Heap_nodes)[1] # delete the head of the heap, and return its position (x and y)
        
        if current_node == positions[end_node]: # if we reached the end node, then construct and return the optimal path  
            path = []
            current_node_position = list(positions.keys())[list(positions.values()).index(current_node)]
            while current_node_position in came_from:
                path.append(current_node_position)
                current_node_position = came_from[current_node_position]
            path.append(source_node)
            path.reverse()
            return path # optimal path

        close_set.add(current_node)  # else
        # find the neighbors of the current node 
        for i, j in neighborhood:
            if positions[i] == current_node:
                current_neighbor = positions[j]
            elif positions[j] == current_node:
                current_neighbor = positions[i]
            else:
                continue # go to next iteration.
            # calculate the gscore of current_neighbor
            gscore_current_neighbor = gscore[current_node] + distanceEuclid(current_node, current_neighbor)
            
            # current neighbor already reached 
            if current_neighbor in close_set:
                continue # next iteration.

            if current_neighbor not in [i[1]for i in Heap_nodes]:
                current_neighbor_position = list(positions.keys())[list(positions.values()).index(current_neighbor)]
                current_node_position = list(positions.keys())[list(positions.values()).index(current_node)] 
                came_from[current_neighbor_position] = current_node_position
                gscore[current_neighbor] = gscore_current_neighbor 
                fscore[current_neighbor] = gscore_current_neighbor + distanceEuclid(current_neighbor, positions[end_node]) 
                heappush(Heap_nodes, (fscore[current_neighbor], current_neighbor)) # adding current_neighbor to the heap

    return False # unreachable "end_node"

# test
path = A_star(1, 4)
print(path)

G = nx.DiGraph()
G.add_nodes_from(positions.keys())

G.add_path(path, color = 'g')
nx.draw(G, pos = positions ,node_size = 1000, width = 3, with_labels = True, edge_color = 'g', node_color = 'y')
nx.draw_networkx_edges(G, pos= positions,
                       edgelist=neighborhood,
                       width=5, alpha=0.1, edge_color='G')

plt.draw()
plt.show()
