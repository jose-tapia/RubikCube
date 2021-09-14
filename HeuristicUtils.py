from RubiksCube import RubiksCube
import CubeUtils
import time

class Distances:
    def __init__(self):
        self._goal_cube = RubiksCube()
        self._memo_distance = dict()
        self._pieces_positions = CubeUtils.cube_pieces_positions

        start = time.time()
        self._precalculate_movements()
        end = time.time()
        print(f'Precalculation : {end-start}')

    def _precalculate_movements(self):
        frontier = []
        
        cube = RubiksCube()

        for idx in range(len(self._pieces_positions)):
            colors = cube.get_colors(self._pieces_positions[idx])
            frontier.append([idx, colors, 0])
            self._memo_distance[str([idx, colors])] = 0
        
        all_movements = CubeUtils.get_all_movements()

        while frontier:
            idx, colors, dist = frontier.pop(0)

            # Set position
            positions_to_erase = cube.find_piece(colors)
            cube.erase_piece(positions_to_erase)
            cube.set_piece(self._pieces_positions[idx], colors)

            for movement in all_movements:
                cube.apply_movement(movement)
                piece = cube.find_piece(colors)
                
                idx_next = self._pieces_positions.index(piece)
                colors_next = cube.get_colors(piece)
                
                if str([idx_next, colors_next]) not in self._memo_distance:
                    frontier.append([idx_next, colors_next, dist + 1])
                    self._memo_distance[str([idx_next, colors_next])] = dist + 1

                cube.erase_piece(piece)
                cube.set_piece(self._pieces_positions[idx], colors)

    def get_movements_average(self, cube):
        cost_sum = 0
        for idx in range(len(self._pieces_positions)):
            colors = cube.get_colors(self._pieces_positions[idx])
            cost_sum += self._memo_distance[str([idx, colors])]
        
        #return cost_sum / len(self._pieces_positions)
        return cost_sum / 4

    def get_manhattan_3D(self, cube):
        cost_sum = 0
        for idx in range(len(self._pieces_positions)):
            x, y, z = CubeUtils.cube_tridimensioanl_positions[idx]

            colors = cube.get_colors(self._pieces_positions[idx])
            piece = self._goal_cube.find_piece(colors)
            idx_f = self._pieces_positions.index(piece)

            x_f, y_f, z_f = CubeUtils.cube_tridimensioanl_positions[idx_f]

            cost_sum += abs(x_f - x) + abs(y_f - y) + abs(z_f - z)
        
        #return cost_sum / len(self._pieces_positions)
        return cost_sum / 6

if __name__ == '__main__':
    scramble = CubeUtils.create_scramble()[:3]
    cube = RubiksCube(scramble)

    distance = Distances()
    print(distance.get_manhattan_3D(cube))
    print(distance.get_movements_average(cube))
