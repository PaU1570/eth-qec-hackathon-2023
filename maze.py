import numpy as np
import itertools
import random
import matplotlib.pyplot as plt

def dfs(grid, curr, end, visited):
    if curr == end:
        return True
    
    visited.add(curr)
    
    row, col = curr
    
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        next_row, next_col = row + dr, col + dc
        
        if 0 <= next_row < 3 and 0 <= next_col < 3 and grid[next_row][next_col] == 0 and (next_row, next_col) not in visited:
            if dfs(grid, (next_row, next_col), end, visited):
                return True
    
    return False

def has_path_of_zeros(grid):
    path = False
    corners = [(0, 0), (0, len(grid)-1), (len(grid)-1, 0), (len(grid)-1, len(grid)-1)]
    for i, j in corners:
        for k, l in corners:
            if (i, j) != (k, l) and grid[i][j] == 0 and grid[k][l] == 0:
                if dfs(grid, (i, j), (k, l), set()):
                    path = True
    return path
def check(grids):
    checks = []
    for grid in grids:
        checks.append(has_path_of_zeros(grid))
    return checks

def generate_maze_field():
    n = 3
    # Generate all possible combinations of 0's and 1's for a single cell
    cell_values = [0, 1]
    cell_combinations = list(itertools.product(cell_values, repeat=3))
    grid_combinations = list(itertools.product(cell_combinations, repeat=3))
    #print(grid_combinations)
    random.shuffle(grid_combinations)
    for i, a in enumerate(grid_combinations):
        if not has_path_of_zeros(a):
            grid_combinations.pop(i)
        if len(grid_combinations) == 440:
            break
    random.shuffle(grid_combinations)
    #print(len(grid_combinations))
    #print(grid_combinations)


    maze_fields = []
    val = []
    N = 0
    for a in grid_combinations:
        maze_field = []
        for j, b in enumerate(a):
            for k, c in enumerate(b):
                maze_field.append(c)
        maze_fields.append(maze_field)
        val.append(has_path_of_zeros(a))
    #print(maze_fields)
    #print(val)
    #print(len(val))
    index = 0
    for i in val:
        if i:
            index += 1
    #print(index)
    #random.shuffle(maze_fields)
    #print(maze_fields)

    return maze_fields, grid_combinations

def encode_data(maze_field, circuit):
    #for entry, index in zip(data_g, range(len(data_g))):
    #    circuit.rx(entry * 2 * np.pi / 3, index)
        
    for index, entry in enumerate(maze_field):
        circuit.rx(entry*np.pi, index)
                   
    return circuit

def add_single_qubit_gates(params, circuit):
    # corners (green)
    for i in [0, 2, 6, 8]:
        circuit.rx(params[0], i)
        circuit.ry(params[1], i)
    # edges (red)
    for i in [1, 3, 5, 7]:
        circuit.rx(params[2], i)
        circuit.ry(params[3], i)
    
    # middle (yellow)
    circuit.rx(params[4], 4)
    circuit.ry(params[5], 4)
    
    return circuit

def ns_add_single_qubit_gates(params, circuit):
    # corners (green)
    for i in range(9):
        circuit.rx(params[2*i], i)
        circuit.ry(params[2*i+1], i)
    
    return circuit

def add_two_qubit_gates(params, circuit):
    # corners (green)
    corner_qubits = [0,2,6,8]
    edge_qubits = [1,3,5,7]
    center_qubit = 4
    
    # yellow two-qubit gates
    for i in corner_qubits:
        circuit.cry(params[0], center_qubit, i, label = 'yellow')
        
    # red two-qubit gates
    for i in edge_qubits:
        circuit.cry(params[1], i, center_qubit, label = 'red')
    
    # green two-qubit gates
    for i in edge_qubits:
        if i == 1 or i == 7:
            circuit.cry(params[2], i-1, i, label = 'green')
            circuit.cry(params[2], (i+1), i, label = 'green')
        else:
            circuit.cry(params[2], i-3, i, label = 'green')
            circuit.cry(params[2], (i+3), i, label = 'green')
    
    
    return circuit

def ns_add_two_qubit_gates(params, circuit):
    # corners (green)
    corner_qubits = [0,2,6,8]
    edge_qubits = [1,3,5,7]
    center_qubit = 4
    
    # yellow two-qubit gates
    for idx, i in enumerate(corner_qubits):
        circuit.cry(params[idx], center_qubit, i, label = 'yellow')
        
    # red two-qubit gates
    for idx, i in enumerate(edge_qubits):
        circuit.cry(params[4 + idx], i, center_qubit, label = 'red')
    
    # green two-qubit gates
    for idx, i in enumerate(edge_qubits):
        if i == 1 or i == 7:
            circuit.cry(params[8 + 2*idx], i-1, i, label = 'green')
            circuit.cry(params[8 + 2*idx+1], (i+1), i, label = 'green')
        else:
            circuit.cry(params[8 + 2*idx], i-3, i, label = 'green')
            circuit.cry(params[8 + 2*idx+1], (i+3), i, label = 'green')
    
    
    return circuit

def plot_maze(maze):
    fig, ax = plt.subplots(figsize = (4,4))
    #  0  1  2
    #  3  4  5
    #  6  7  8

    matrix = np.reshape(maze, (3,3))
    if has_path_of_zeros(matrix):
        c = 'Greens'
    else:
        c = 'Reds'
    ax.imshow(matrix, cmap = c)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()