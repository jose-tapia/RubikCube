from copy import deepcopy
from heapq import heappop, heappush
import time

from HeuristicUtils import Distances
from RubiksCube import RubiksCube
import CubeUtils
import json

movements = {}

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
        Implementation of the A* algorithm to solve the Rubik's cube.
        Params: 
          - initial_state: The Rubik's cube initial state
          - heuristic: Function that takes a Rubik's cube and returns an estimation of how many movements are needed to solve it
    """
    # Rubik's cube solved - Represents the objective state 
    goal_state = RubiksCube()

    # Initialize the lists in which we are going to store the nodes we are creating
    #  - explored: the nodes already explored (expanded)
    #  - frontier: the nodes to be explored (not expanded yet, but are obtained from the explored nodes
    frontier = []
    explored = set()

    # Initialize initial state and append it to the frontier
    initial_node = Node(initial_state, cost = heuristic(initial_state))
    heappush(frontier, initial_node)
    
    # Check if frontier still has elements to visit
    all_movements = CubeUtils.get_all_movements()
    while len(frontier) > 0:
        # Takes Rubik's cube with minimum estimated cost from the frontier
        current_node = heappop(frontier)

        # If the node was already explored, we ommited it
        if str(current_node.state) in explored:
            continue
        explored.add(str(current_node.state))

        # Check if the node is the goal
        if current_node.state == goal_state:
            return current_node

        # Expand the actual state applying all the movements
        for movement in all_movements:
            # Check if the movement is valid (considering the last movement applied to the cube)
            if reduce_factor_branch(movement, current_node.movement):
                continue            

            # Generate the next state, applying the corresponding movement
            next_state = deepcopy(current_node.state)
            next_state.apply_movement(movement)

            # Verify if the cube was explored
            if str(next_state) in explored:
                continue
            
            # Store information needed to represent the state
            next_node = Node(next_state, 
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            (current_node.level + 1) + heuristic(next_state))

            # Insert the node to the frontier
            heappush(frontier, next_node)
    return None

def get_solution(path):
    # Obtain the solution path
    solution = []
    while path.parent:
        solution.append(path.movement)
        path = path.parent
    solution.reverse()
    return solution

if __name__ == '__main__':
    # Initialization of the Rubik's cube to be solved
    distances = Distances()
    scramble = CubeUtils.create_scramble(9)
    # Substitute 'scramble' with the array of movements wanted 
    cube = RubiksCube(scramble)

    # Definition of the heuristics 
    cost_function_manhattan = lambda cube: distances.get_manhattan_3D(cube) / 6
    cost_function_movements = lambda cube: distances.get_movements_average(cube) / 4

    print(f'Initial scramble : {scramble}, size {len(scramble)}')
    # Search solution
    start = time.time()
    path = search(cube, cost_function_movements)
    end = time.time()

    # Visualize solution path
    print(path)
    print(f'Time : {end-start}')

    solution = get_solution(path)

    # Print solution array
    print(f'Initial scramble : {scramble}, size {len(scramble)}')
    print(f'Solution :\t   {get_solution(path)}, size {len(get_solution(path))}')
    movements["scramble"] = scramble
    movements["solution"] = solution
    with open('movements.json', 'w') as fp:
        json.dump(movements, fp,  indent=4)