import numpy as np
import random

# helper function to determine valid tic tac toe board positions
def get_winner(board):
        # Check the board for any winning combinations
    winning_combinations = [
        # Rows
        (0, 1, 2),
        (7, 8, 3),
        (6, 5, 4),
        # Columns
        (0, 7, 6),
        (1, 8, 5),
        (2, 3, 4),
        # Diagonals
        (0, 8, 4),
        (2, 8, 6),
    ]
    
    x_wins = False
    o_wins = False
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            if board[combo[0]] == 'x':
                return [0,0,1]
            else:
                return [1,0,0]
    return [0,1,0]
    

def is_valid_tic_tac_toe(board):
    # Check that the board has exactly 9 elements
    if len(board) != 9:
        return False
    
    # Count the number of 'x' and 'o' on the board
    count_x = board.count('x')
    count_o = board.count('o')
    
    # Check that the difference in count between 'x' and 'o' is 0 or 1
    if abs(count_x - count_o) > 1:
        return False
    
    # Check the board for any winning combinations
    winning_combinations = [
        # Rows
        (0, 1, 2),
        (7, 8, 3),
        (6, 5, 4),
        # Columns
        (0, 7, 6),
        (1, 8, 5),
        (2, 3, 4),
        # Diagonals
        (0, 8, 4),
        (2, 8, 6),
    ]
    
    x_wins = False
    o_wins = False
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            if board[combo[0]] == 'x':
                x_wins = True
            else:
                o_wins = True
    
    
    # Check that the board is a valid final board configuration
    if (x_wins and count_x != count_o + 1) or (o_wins and count_x != count_o):
        return False

    # All checks have passed, so the board is valid
    return True
  
    
def generate_tic_tac_toe_configs(mode = 'all'):
    valid_configs = []
    winners = []
    
    # Generate all possible configurations of the board
    for i in range(3**9):
        board = []
        for j in range(9):
            symbol = ''
            if i % 3 == 0:
                symbol = 'x'
            elif i % 3 == 1: 
                symbol = 'o'
            board.append(symbol)
            i //= 3
        
        # Check if the configuration is valid
        if is_valid_tic_tac_toe(board):
            if mode == 'all':
                valid_configs.append(board)
                winners.append(get_winner(board))
            elif mode == 'decisive' and get_winner(board) != [0,1,0]:
                valid_configs.append(board)
                winners.append(get_winner(board))
            elif mode == 'draws' and get_winner(board) == [0,1,0]:
                valid_configs.append(board)
                winners.append(get_winner(board))
            elif mode == 'x_wins' and get_winner(board) == [0,0,1]:
                valid_configs.append(board)
                winners.append(get_winner(board))
            elif mode == 'o_wins' and get_winner(board) == [1,0,0]:
                valid_configs.append(board)
                winners.append(get_winner(board))

                
    
    return valid_configs, winners



def load_boards(include_draws):
    boards, winners = generate_tic_tac_toe_configs(mode = 'decisive')

    if include_draws:
        draw_boards, draw_winners = generate_tic_tac_toe_configs(mode = 'draws')
        # do the shuffle for draws
        temp = list(zip(draw_boards, draw_winners))
        random.shuffle(temp)
        draw_boards, draw_winners = zip(*temp)
        draw_boards, draw_winners = list(draw_boards), list(draw_winners)

        # pick same amount of draws as x/o wins
        draw_boards = draw_boards[:len(boards)//2]
        draw_winners = draw_winners[:len(boards)//2]

        boards += draw_boards
        winners += draw_winners

        # shuffle again
        temp = list(zip(boards, winners))
        random.shuffle(temp)
        boards, winners = zip(*temp)
        boards, winners = list(boards), list(winners)

    return boards, winners


## FUNCTIONS TO SET UP CIRCUIT
def encode_data(tic_tac_toe_field, circuit):
    data_g = [1 if entry == 'x' else -1 if entry == 'o' else 0 for entry in tic_tac_toe_field ]
    #for entry, index in zip(data_g, range(len(data_g))):
    #    circuit.rx(entry * 2 * np.pi / 3, index)
        
    for index, entry in enumerate(data_g):
        circuit.rx(entry * 2 * np.pi / 3, index)
                   
    return circuit

def add_single_qubit_gates(params, circuit):
    # corners (green)
    for i in [0, 2, 4, 6]:
        circuit.rx(params[0], i)
        circuit.ry(params[1], i)
    # edges (red)
    for i in [1, 3, 5, 7]:
        circuit.rx(params[2], i)
        circuit.ry(params[3], i)
    
    # middle (yellow)
    circuit.rx(params[4], 8)
    circuit.ry(params[5], 8)
    
    return circuit

def ns_add_single_qubit_gates(params, circuit):
    # corners (green)
    for i in range(9):
        circuit.rx(params[2*i], i)
        circuit.ry(params[2*i+1], i)
    
    return circuit

def add_two_qubit_gates(params, circuit):
    # corners (green)
    corner_qubits = [0,2,4,6]
    edge_qubits = [1,3,5,7]
    center_qubit = 8
    
    # yellow two-qubit gates
    for i in corner_qubits:
        circuit.cry(params[0], center_qubit, i, label = 'yellow')
        
    # red two-qubit gates
    for i in edge_qubits:
        circuit.cry(params[1], i, center_qubit, label = 'red')
    
    # green two-qubit gates
    for i in edge_qubits:
        circuit.cry(params[2], i-1, i, label = 'green')
        circuit.cry(params[2], (i+1) % 8, i, label = 'green')
    
    
    return circuit

def ns_add_two_qubit_gates(params, circuit):
    # corners (green)
    corner_qubits = [0,2,4,6]
    edge_qubits = [1,3,5,7]
    center_qubit = 8
    
    # yellow two-qubit gates
    for idx, i in enumerate(corner_qubits):
        circuit.cry(params[idx], center_qubit, i, label = 'yellow')
        
    # red two-qubit gates
    for idx, i in enumerate(edge_qubits):
        circuit.cry(params[4 + idx], i, center_qubit, label = 'red')
    
    # green two-qubit gates
    for idx, i in enumerate(edge_qubits):
        circuit.cry(params[8 + 2*idx], i-1, i, label = 'green')
        circuit.cry(params[8 + 2*idx+1], (i+1) % 8, i, label = 'green')
    
    
    return circuit

