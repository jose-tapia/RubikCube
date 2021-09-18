from copy import deepcopy
import time

from RubiksCube import RubiksCube
import CubeUtils



class Distances:
    "Class that serve to calculate the heuristics for solve the rubik's cube with A* algorithm"
    def __init__(self, goal_cube = RubiksCube()):
        # Set the goal cube
        self._goal_cube = goal_cube
        self._memo_distance = dict()
        self._pieces_positions = CubeUtils.cube_pieces_positions

        # Precalculate the distance movements
        start = time.time()
        self._precalculate_movements()
        end = time.time()
        print(f'Precalculation : {end-start}')

    def _precalculate_movements(self):
        "Using a BFS, precalculate how many movements a piece needs to do to reach its goal state"
        # Start frontier of BFS
        frontier = []

        # Set initial pieces with cost 0
        cube = deepcopy(self._goal_cube)

        for idx in range(len(self._pieces_positions)):
            colors = cube.get_colors(self._pieces_positions[idx])
            frontier.append([idx, colors, 0])
            self._memo_distance[str([idx, colors])] = 0
        
        # While frontier has elements, process them
        all_movements = CubeUtils.get_all_movements()
        while frontier:
            # Obtain next piece to explore
            idx, colors, dist = frontier.pop(0)

            # Set piece in the cube
            positions_to_erase = cube.find_piece(colors)
            cube.erase_piece(positions_to_erase)
            cube.set_piece(self._pieces_positions[idx], colors)

            # Get next pieces
            for movement in all_movements:
                cube.apply_movement(movement)
                curr_piece = cube.find_piece(colors)
                
                idx_next = self._pieces_positions.index(curr_piece)
                colors_next = cube.get_colors(curr_piece)
                
                # If next piece is not visited yet
                if str([idx_next, colors_next]) not in self._memo_distance:
                    # Add it to the frontier and store its distance
                    frontier.append([idx_next, colors_next, dist + 1])
                    self._memo_distance[str([idx_next, colors_next])] = dist + 1

                # In all cases, erase the moved piece and
                # place it in the original position again
                cube.erase_piece(curr_piece)
                cube.set_piece(self._pieces_positions[idx], colors)

    def get_movements_average(self, cube):
        "Given a rubik's cube, sum the number of movements that each piece needs to reach it's goal state"
        cost_sum = 0
        for idx in range(len(self._pieces_positions)):
            # Get colors of the piece idx
            colors = cube.get_colors(self._pieces_positions[idx])
            # Get distance to the goal position 
            cost_sum += self._memo_distance[str([idx, colors])]
        
        return cost_sum 

    def get_manhattan_3D(self, cube):
        "Given a rubik's cube, sum the manhattan distane between each piece and its position in the goal state"
        cost_sum = 0
        for idx in range(len(self._pieces_positions)):
            x, y, z = CubeUtils.cube_tridimensioanl_positions[idx]

            # Get colors of the piece idx
            colors = cube.get_colors(self._pieces_positions[idx])
            # Find piece with such combination of colors in the goal_cube
            piece = self._goal_cube.find_piece(colors)
            idx_f = self._pieces_positions.index(piece)

            x_f, y_f, z_f = CubeUtils.cube_tridimensioanl_positions[idx_f]

            # Get manhattan distance
            cost_sum += abs(x_f - x) + abs(y_f - y) + abs(z_f - z)
        
        return cost_sum 

if __name__ == '__main__':
    scramble = CubeUtils.create_scramble()[:3]
    cube = RubiksCube(scramble)

    distance = Distances()
    print(distance.get_manhattan_3D(cube))
    print(distance.get_movements_average(cube))
