import numpy as np
from numpy.core.numeric import Inf
from Cube import RubiksCube
from CubeUtils import create_scramble, get_all_movements, get_basic_prefix
from HeuristicUtils import DistancePieces
from copy import deepcopy
from heapq import heappush, heappop
import time

distances = DistancePieces()

class Node:
    def __init__(self, state: RubiksCube, parent = None, level = 0, operation = None, cost = 0):
        self.state = state 
        self.parent = parent 
        self.level = level
        self.operation = operation 
        self.cost = cost
    
    def __str__(self):
        if self.parent == None:
            return f' Initial state:\n {self.state}'
        return f'{self.parent}\n Applying operation {self.operation}:\n {self.state}'

    def __eq__(self, other):
        if other is None:
            return False
        return str(self.state) == str(other.getState())

    def __lt__(self, other):
        return self.cost < other.getCost()

    def getState(self):
        return self.state 
    def getParent(self):
        return self.parent 
    def getLevel(self):
        return self.level
    def getOperation(self):
        return self.operation
    def getCost(self):
        return self.cost

def getNextNode(frontier, searchType):
    if searchType == 'BFS':
        return frontier.pop(0)
    elif searchType == 'DFS':
        return frontier.pop()
    elif searchType == 'A*':
        return heappop(frontier)
    return None

def pushNextNode(frontier, node, searchType):
    if searchType == 'BFS' or searchType == 'DFS':
        frontier.push(node)
    else:
        heappush(frontier, node)

def get_cost(cube, searchType, heuristic, additional_cost = 0):
    if searchType == 'DFS' or searchType == 'BFS':
        return additional_cost
    if searchType == 'A*':
        if heuristic == 'movements':
            return distances.get_num_movements(cube)/8 + additional_cost
        if heuristic == 'manhattan3D':
            return distances.get_manhattan_3D(cube) + additional_cost
    return Inf

def search(initial_state, searchType = 'BFS', heuristic = ''):
    frontier = []
    visited = set()
    explored = set()

    initial_node = Node(initial_state, cost = get_cost(initial_state, searchType, heuristic, 0))
    pushNextNode(frontier, initial_node, searchType)

    goal = RubiksCube()

    while frontier:
        actual_node = getNextNode(frontier, searchType)

        if str(actual_node.getState()) in explored:
            continue
        explored.add(str(actual_node.getState()))

        if str(actual_node.getState()) == str(goal):
            return actual_node

        movements = get_all_movements()
        for mov in movements:
            if get_basic_prefix(mov) == get_basic_prefix(actual_node.getOperation()):
                continue

            next_cube = deepcopy(actual_node.getState())
            next_cube.apply_movement(mov)
            next_node = Node(next_cube, actual_node, actual_node.getLevel() + 1, mov, get_cost(initial_state, searchType, heuristic, actual_node.getLevel()+1))

            if str(next_cube) not in visited:
                visited.add(str(next_cube))
                pushNextNode(frontier, next_node, searchType)
    return None        

if __name__ == '__main__':
    

    np.random.seed(1)
    scramble = create_scramble()[:3]

    cube = RubiksCube(scramble)
    #path = search(cube, 'A*', 'manhattan3D')
    start = time.time()
    path = search(cube, 'A*', 'movements')
    
    end = time.time()
    print(path)
    print(end - start)
