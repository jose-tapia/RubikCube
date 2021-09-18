from copy import deepcopy
from heapq import heappop, heappush 
import time 

from HeuristicUtils import Distances
from RubiksCube import RubiksCube
 #import Node, reduce_factor_branch
import CubeUtils
import Search

class BidirectionalNode(Search.Node):
    "Class that wraps the state and its necessary information to represent it"
    def __init__(self, state, group, parent = None, level = 0, movement = None, cost = 0):
        super().__init__(state, parent, level, movement, cost)
        # Store if belongs to initial search or end search
        self.group = group

def bidirectional_search(initial_state, heuristic_start, heuristic_end):
    frontier = []
    explored_start = dict()
    explored_end = dict()
    
    goal_state = RubiksCube()

    initial_node = BidirectionalNode(initial_state, 'start', cost = heuristic_start(initial_state))
    final_node = BidirectionalNode(goal_state, 'end', cost = heuristic_end(goal_state))

    heappush(frontier, initial_node)
    heappush(frontier, final_node)

    all_movements = CubeUtils.get_all_movements()
    while frontier:
        current_node = heappop(frontier)

        if current_node.group == 'start':
            if str(current_node.state) in explored_start:
                continue
            explored_start[str(current_node.state)] = current_node

            if str(current_node.state) in explored_end:
                return current_node, explored_end[str(current_node.state)]
        else:
            if str(current_node.state) in explored_end:
                continue
            explored_end[str(current_node.state)] = current_node

            if str(current_node.state) in explored_start:
                return explored_start[str(current_node.state)], current_node
        
        for movement in all_movements:
            if Search.reduce_factor_branch(movement, current_node.movement):
                continue    

            next_state = deepcopy(current_node.state)
            next_state.apply_movement(movement)

            next_node = None
            if current_node.group == 'start':
                if str(next_state) in explored_start:
                    continue
                
                next_node = BidirectionalNode(next_state, 
                            'start',
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            (current_node.level + 1) + heuristic_start(next_state))
            else:
                if str(next_state) in explored_end:
                    continue

                next_node = BidirectionalNode(next_state, 
                            'end',
                            current_node, 
                            current_node.level + 1, 
                            movement, 
                            (current_node.level + 1) + heuristic_end(next_state))

            if next_node is not None:
                heappush(frontier, next_node)

def get_solution(start, end):
    path_start = Search.get_solution(start)

    path_end = Search.get_solution(end)
    path_end.reverse()
    good_path_end = []
    for movement in path_end:
        basic_movement = CubeUtils.get_movement_prefix(movement)
        suffix_movement = CubeUtils.get_movement_suffix(movement)
        if suffix_movement == '':
            suffix_movement = "'"
        elif suffix_movement == "'":
            suffix_movement = ''
        good_path_end.append(basic_movement + suffix_movement)

    return path_start + good_path_end

if __name__ == '__main__':
    scramble = CubeUtils.create_scramble(8)
    cube = RubiksCube(scramble)
    
    print(f'Scramble: {scramble}, size: {len(scramble)}')

    distances_normal = Distances()
    distances_reverse = Distances(cube)

    heuristic_start = lambda cube: distances_normal.get_manhattan_3D(cube) / 8
    heuristic_end = lambda cube: distances_reverse.get_manhattan_3D(cube) / 8

    start_time = time.time()
    start_node, end_node = bidirectional_search(cube, heuristic_start, heuristic_end)
    end_time = time.time()

    path = get_solution(start_node, end_node)

    print(f'Solution: {path}, size: {len(path)}')
    print('Initial state:')
    print(cube)
    for movement in path:
        print(f'Applying movement {movement}:')
        cube.apply_movement(movement)
        print(cube)

    print(f'Time: {end_time - start_time}')

    print(f'Scramble: {scramble}, size: {len(scramble)}')
    print(f'Solution: {path}, size: {len(path)}')