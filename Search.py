from copy import deepcopy
from heapq import heappop, heappush
import time

from HeuristicUtils import Distances
from RubiksCube import RubiksCube
import CubeUtils



basic_movements = CubeUtils.get_basic_movements()

class Node:
    "Class that wraps the state and its necessary information to represent it"
    def __init__(self, state, parent = None, level = 0, movement = None, cost = 0):
        self.state = state 
        self.parent = parent 
        self.level = level 
        self.movement = movement
        self.cost = cost
    
    def __str__(self):
        if self.parent == None:
            return f' Initial state:\n {self.state}'
        return f'{self.parent}\n Applying movement {self.movement}:\n {self.state}'
    
    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.state == other.state
    
    def __lt__(self, other):
        return self.cost < other.cost

def reduce_factor_branch(movement, past_movement):
    "Observations that reduce the factor branch from 18 to ~12"
    basic_movement = CubeUtils.get_movement_prefix(movement)
    basic_past_movement = CubeUtils.get_movement_prefix(past_movement)

    if basic_past_movement is None:
        return False

    idx_movement = basic_movements.index(basic_movement)
    idx_past_movement = basic_movements.index(basic_past_movement)

    return idx_movement == idx_past_movement or (idx_movement >= 3 and idx_movement == idx_past_movement + 3)
    
def search(initial_state, heuristic):
    """
        Function description:

        Params: 
          - initial_state: 
          - heuristic: 
    """
    ###
    goal_state = RubiksCube()

    ###
    frontier = []
    explored = set()

    ###
    initial_node = Node(initial_state, cost = heuristic(initial_state))
    heappush(frontier, initial_node)
    
    ###
    all_movements = CubeUtils.get_all_movements()
    while frontier:
        ###
        current_node = heappop(frontier)

        ###
        if str(current_node.state) in explored:
            continue
        explored.add(str(current_node.state))

        ###
        if current_node.state == goal_state:
            return current_node

        ###
        for movement in all_movements:
            ###
            if reduce_factor_branch(movement, current_node.movement):
                continue            

            ###
            next_state = deepcopy(current_node.state)
            next_state.apply_movement(movement)

            ###
            if str(next_state) in explored:
                continue
            
            ###
            next_node = Node(next_state, 
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            (current_node.level + 1) + heuristic(next_state))

            ###
            heappush(frontier, next_node)
    return None

def get_solution(path):
    ###
    solution = []
    while path.parent:
        solution.append(path.movement)
        path = path.parent
    solution.reverse()
    return solution

if __name__ == '__main__':
    
    distances = Distances()
    scramble = CubeUtils.create_scramble(8)
    cube = RubiksCube(scramble)

    cost_function_manhattan = lambda cube: distances.get_manhattan_3D(cube) / 6
    cost_function_movements = lambda cube: distances.get_movements_average(cube) / 4

    print(f'Initial scramble : {scramble}, size {len(scramble)}')

    start = time.time()
    path = search(cube, cost_function_movements)
    end = time.time()

    print(path)
    print(f'Time : {end-start}')


    print(f'Initial scramble : {scramble}, size {len(scramble)}')
    print(f'Solution :\t   {get_solution(path)}, size {len(get_solution(path))}')