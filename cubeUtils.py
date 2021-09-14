import numpy as np
import random

colors = ['W', 'O', 'G', 'R', 'B', 'Y']

cube_movements = dict({'U' : [0, 'L', 0, None, 'L'],
                       'D' : [5, 'L', 2, None, 'R'],
                       'L' : [1, 'L', None, 3, 'L'], 
                       'R' : [3, 'L', None, 5, 'R'],
                       'F' : [2, 'L', None, 2, 'R'],
                       'B' : [4, 'L', None, 0, 'L']})

cube_pieces_positions = [[(0, 0, 0), (1, 0, 0), (4, 0, 2)],
                         [(0, 0, 1), (4, 0, 1)],
                         [(0, 0, 2), (3, 0, 2), (4, 0, 0)],
                         [(0, 1, 0), (1, 0, 1)],
                         [(0, 1, 2), (3, 0, 1)],
                         [(0, 2, 0), (1, 0, 2), (2, 0, 0)],
                         [(0, 2, 1), (2, 0, 1)],
                         [(0, 2, 2), (2, 0, 2), (3, 0, 0)],
                         [(1, 1, 0), (4, 1, 2)],
                         [(1, 1, 2), (2, 1, 0)],
                         [(2, 1, 2), (3, 1, 0)],
                         [(3, 1, 2), (4, 1, 0)],
                         [(5, 0, 0), (1, 2, 2), (2, 2, 0)],
                         [(5, 0, 1), (2, 2, 1)],
                         [(5, 0, 2), (2, 2, 2), (3, 2, 0)],
                         [(5, 1, 0), (1, 2, 1)],
                         [(5, 1, 2), (3, 2, 1)],
                         [(5, 2, 0), (1, 2, 0), (4, 2, 2)],
                         [(5, 2, 1), (4, 2, 1)],
                         [(5, 2, 2), (3, 2, 2), (4, 2, 0)]]

def get_basic_movements():
    return list(cube_movements.keys())

def get_movement_suffix(movement):
    if movement is None:
        return None
    elif len(movement) == 1 or len(movement) > 2:
        return ''
    elif movement[1] in ['2', "'"]:
        return movement[1]
    else:
        return None

def get_movement_prefix(movement):
    if movement is None:
        return None
    elif len(movement) == 1:
        return movement
    elif len(movement) > 2:
        # Not supported yet
        return None
    elif get_movement_suffix(movement) is not None:
        return movement[0]
    else:
        return None

def get_all_movements():
    basic_movs = get_basic_movements()
    return [mov + suffix for mov in basic_movs for suffix in ['', '2', "'"]]

def create_scramble():
    movements = get_all_movements()
    #movements = get_basic_movements()
    return random.choices(movements, k = random.randint(20, 35))
