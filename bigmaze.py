import numpy as np
import heapq
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = list() # list of tuples
        self.neighbors = dict() # dict[tuple] -> list of tuples
    
    def get_neighbors(self, node):
        return self.neighbors[node]
    
    def add_node(self, node, neighbors):
        self.nodes.append(node)
        self.neighbors[node] = neighbors

def make_graph(maze):
    ################################
    #  0  1  2  3  4 
    #  5  6  7  8  9
    # 10 11 12 13 14
    # 15 16 17 18 19
    # 20 21 22 23 24

    # nodes are (index, value)

    graph = Graph()
    for i,m in enumerate(maze):

        neighbors = []
        # add left neighbor
        if i % 5 != 0:
            if  maze[i-1] == 0:
                neighbors.append((i-1, maze[i-1]))
        # add right neighbor
        if (i+1)%5 != 0:
            if maze[i+1] == 0:
                neighbors.append((i+1, maze[i+1]))
        # add top neighbor
        if (i-5) >= 0:
            if maze[i-5] == 0:
                neighbors.append((i-5, maze[i-5]))
        # add bottom neighbor
        if (i+5) <= 24:
            if maze[i+5] == 0:
                neighbors.append((i+5, maze[i+5]))

        graph.add_node((i, m), neighbors)

    return graph

def path_exists(graph, source, targets):
    # source must be tuple, targets is list of tuples

    dist = dict()
    prev = dict()    
    
    pq = list()
    
    for node in graph.nodes:
        dist[node] = np.inf
        prev[node] = None
    
    dist[source] = 0
    pq.append((0, source))
        
    while len(pq) > 0:
        d, u = heapq.heappop(pq)
        #print(u)
        if u[0] in targets:
            return True
            
        if d > dist[u]:
            continue
            
        for v in graph.get_neighbors(u):
            alt = d + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))
                
    for t in targets:
        if dist[t] < np.inf:
            return True
    return False

def check_path(maze):
    g = make_graph(maze)
    if maze[0] == 0:
        if path_exists(g, (0, 0), [(4, maze[4]), (20, maze[20]), (24, maze[24])]):
            return True
    if maze[4] == 0:
        if path_exists(g, (4, 0), [(0, maze[0]), (20, maze[20]), (24, maze[24])]):
            return True
    if maze[20] == 0:
        if path_exists(g, (20, 0), [(0, maze[0]), (4, maze[4]), (24, maze[24])]):
            return True
    return False

def generate_maze_field(size):
    maze_fields = []
    expected_results = []
    for i in range(size):
        maze = np.random.choice([0,1], size = 25, p = [0.6, 0.4])
        maze_fields.append(maze)
        expected_results.append(check_path(maze))
    return maze_fields, expected_results

def plot_maze(maze):
    fig, ax = plt.subplots(figsize = (8,8))
    #  0  1  2  3  4 
    #  5  6  7  8  9
    # 10 11 12 13 14
    # 15 16 17 18 19
    # 20 21 22 23 24
    matrix = np.reshape(maze, (5,5))
    if check_path(maze):
        c = 'Greens'
    else:
        c = 'Reds'
    ax.imshow(matrix, cmap = c)
    #ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

def encode_data(maze_field, circuit):
        
    for index, entry in enumerate(maze_field):
        circuit.rx(entry*np.pi, index)
                   
    return circuit

def add_single_qubit_gates(params, circuit):
    # inner corners
    for i in [6, 8, 16, 18]:
        circuit.rx(params[0], i)
        circuit.ry(params[1], i)
    # inner edges
    for i in [7, 13, 11, 17]:
        circuit.rx(params[2], i)
        circuit.ry(params[3], i)
    
    # middle
    circuit.rx(params[4], 12)
    circuit.ry(params[5], 12)

    # outer corners
    for i in [0, 4, 20, 24]:
        circuit.rx(params[6], i)
        circuit.ry(params[7], i)

    # outer edges
    for i in [2, 10, 14, 22]:
        circuit.rx(params[8], i)
        circuit.ry(params[9], i)

    # rest
    for i in [1, 3, 5, 9, 15, 19, 21, 23]:
        circuit.rx(params[10], i)
        circuit.ry(params[11], i)
    
    
    return circuit

def add_two_qubit_gates(params, circuit):

    #  0  1  2  3  4 
    #  5  6  7  8  9
    # 10 11 12 13 14
    # 15 16 17 18 19
    # 20 21 22 23 24

    # corners (green)
    inner_corner_qubits = [6, 8, 16, 18]
    inner_edge_qubits = [7, 13, 11, 17]
    center_qubit = 12
    outer_corner_qubits = [0, 4, 20, 24]
    outer_edge_qubits = [2, 10, 14, 22]
    rest_qubits = [1, 3, 5, 9, 15, 19, 21, 23]
    
    # inner 3x3 gates
    # yellow two-qubit gates
    for i in inner_corner_qubits:
        circuit.cry(params[0], center_qubit, i, label = 'yellow')
        
    # red two-qubit gates
    for i in inner_edge_qubits:
        circuit.cry(params[1], i, center_qubit, label = 'red')
    
    # green two-qubit gates
    for i in inner_edge_qubits:
        if i == 7 or i == 17:
            circuit.cry(params[2], i-1, i, label = 'green')
            circuit.cry(params[2], (i+1), i, label = 'green')
        else:
            circuit.cry(params[2], i-5, i, label = 'green')
            circuit.cry(params[2], (i+5), i, label = 'green')

    # extra 5x5 gates

    # outer corners with inner corners
    for outer, inner in zip(outer_corner_qubits, inner_corner_qubits):
        circuit.cry(params[3], outer, inner)

    # outer edges with inner edges
    for outer, inner in zip(outer_edge_qubits, inner_edge_qubits):
        circuit.cry(params[4], inner, outer)

    # grey with white
    for i in outer_corner_qubits:
        if i == 0 or i == 20:
            circuit.cry(params[5], i, i+1)
        if i == 4 or i == 24:
            circuit.cry(params[5], i, i-1)
        if i == 0 or i == 4:
            circuit.cry(params[5], i, i+5)
        if i == 20 or i == 24:
            circuit.cry(params[5], i, i-5)

    # yellow with grey
    for i in outer_edge_qubits:
        if i == 2 or i == 22:
            circuit.cry(params[6], i-1, i)
            circuit.cry(params[6], i+1, i)
        if i == 10 or i == 14:
            circuit.cry(params[6], i-5, i)
            circuit.cry(params[6], i+5, i)

    # black with grey
    for i in inner_corner_qubits:
        if i == 6 or i == 8:
            circuit.cry(params[7], i, i-5)
        if i == 16 or i == 18:
            circuit.cry(params[7], i, i+5)
        if i == 6 or i == 16:
            circuit.cry(params[7], i, i-1)
        if i == 8 or i == 18:
            circuit.cry(params[7], i, i+1)

    # blue with grey
    circuit.cry(params[8], 1, 7)
    circuit.cry(params[8], 3, 7)

    circuit.cry(params[8], 5, 11)
    circuit.cry(params[8], 15, 11)

    circuit.cry(params[8], 9, 13)
    circuit.cry(params[8], 19, 13)

    circuit.cry(params[8], 21, 17)
    circuit.cry(params[8], 23, 17)
    
    
    return circuit





