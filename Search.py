from HeuristicUtils import Distances
from RubiksCube import RubiksCube
import CubeUtils
from heapq import heappop, heappush
import time
from copy import deepcopy

distances = Distances()

basic_movements = CubeUtils.get_basic_movements()

class Node:
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
    basic_movement = CubeUtils.get_movement_prefix(movement)
    basic_past_movement = CubeUtils.get_movement_prefix(past_movement)

    if basic_past_movement is None:
        return False

    idx_movement = basic_movements.index(basic_movement)
    idx_past_movement = basic_movements.index(basic_past_movement)

    return idx_movement == idx_past_movement or (idx_movement >= 3 and idx_movement == idx_past_movement + 3)
    
def search(initial_state, search_functions):
    goal_state = RubiksCube()

    frontier = []
    explored = set()

    initial_node = Node(initial_state, cost = search_functions['cost_function'](initial_state, 0))
    search_functions['push_state'](initial_node, frontier)

    all_movements = CubeUtils.get_all_movements()
    while frontier:
        current_node = search_functions['pop_state'](frontier)

        if str(current_node.state) in explored:
            continue
        explored.add(str(current_node.state))

        if current_node.state == goal_state:
            return current_node

        for movement in all_movements:
            if reduce_factor_branch(movement, current_node.movement):
                continue            

            next_state = deepcopy(current_node.state)
            next_state.apply_movement(movement)

            if str(next_state) in explored:
                continue

            next_node = Node(next_state, 
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            search_functions['cost_function'](next_state, current_node.level + 1))

            search_functions['push_state'](next_node, frontier)
    return None

def get_solution(path):
    solution = []
    while path.parent:
        solution.append(path.movement)
        path = path.parent
    solution.reverse()
    return solution

if __name__ == '__main__':
    # Size 8 works with movements
    scramble = CubeUtils.create_scramble()[:10]
    cube = RubiksCube(scramble)

    push_state_heap = lambda node, frontier: heappush(frontier, node)
    push_state_list = lambda node, frontier: frontier.append(node)

    pop_state_heap = lambda frontier: heappop(frontier)
    pop_state_dfs = lambda frontier: frontier.pop()
    pop_state_bfs = lambda frontier: frontier.pop(0)

    cost_function_manhattan = lambda cube, cost: cost + distances.get_manhattan_3D(cube)
    cost_function_movements = lambda cube, cost: cost + distances.get_movements_average(cube)
    cost_function_default = lambda _, cost: cost


    search_functions_dfs = dict({
        'push_state': push_state_list,
        'pop_state': pop_state_dfs,
        'cost_function': cost_function_default})
    
    search_functions_bfs = dict({
        'push_state': push_state_list,
        'pop_state': pop_state_bfs,
        'cost_function': cost_function_default})
    
    search_functions_Astar_movement = dict({
        'push_state': push_state_heap,
        'pop_state': pop_state_heap,
        'cost_function': cost_function_movements})
    
    search_functions_Astar_manhattan = dict({
        'push_state': push_state_heap,
        'pop_state': pop_state_heap,
        'cost_function': cost_function_manhattan})



    print(f'Initial scramble : {scramble}, size {len(scramble)}')

    start = time.time()
    path = search(cube, search_functions_Astar_movement)
    end = time.time()

    print(path)
    print(f'Time : {end-start}')
    

    print(f'Initial scramble : {scramble}, size {len(scramble)}')
    print(f'Solution :\t   {get_solution(path)}, size {len(get_solution(path))}')
