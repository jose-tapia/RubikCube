from HeuristicUtils import Distances
from RubiksCube import RubiksCube
import CubeUtils
from heapq import heappop, heappush
import time
from copy import deepcopy

distances = Distances()

class Node:
    def __init__(self, state, parent = None, level = 0, movement = '', cost = 0):
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

def search(initial_state, push_state, pop_state, cost_function):
    goal_state = RubiksCube()

    frontier = []
    explored = set()

    initial_node = Node(initial_state, cost = cost_function(initial_state, 0))
    push_state(initial_node, frontier)

    all_movements = CubeUtils.get_all_movements()
    while frontier:
        current_node = pop_state(frontier)

        if str(current_node.state) in explored:
            continue
        explored.add(str(current_node.state))

        if current_node.state == goal_state:
            return current_node

        for movement in all_movements:
            next_state = deepcopy(current_node.state)
            next_state.apply_movement(movement)

            if str(next_state) in explored:
                continue

            next_node = Node(next_state, 
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            cost_function(next_state, current_node.level + 1))

            push_state(next_node, frontier)
    return None



if __name__ == '__main__':
    scramble = CubeUtils.create_scramble()[:7]
    cube = RubiksCube(scramble)

    push_state_heap = lambda node, frontier: heappush(frontier, node)
    push_state_list = lambda node, frontier: frontier.append(node)

    pop_state_heap = lambda frontier: heappop(frontier)
    pop_state_dfs = lambda frontier: frontier.pop()
    pop_state_bfs = lambda frontier: frontier.pop(0)

    cost_function_manhattan = lambda cube, cost: cost + distances.get_manhattan_3D(cube)
    cost_function_movements = lambda cube, cost: cost + distances.get_movements_average(cube)
    cost_function_default = lambda _, cost: cost

    start = time.time()
    path = search(cube, push_state_heap, pop_state_heap, cost_function_movements)
    end = time.time()

    print(path)
    print(f'Time : {end-start}')