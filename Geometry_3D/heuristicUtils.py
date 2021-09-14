from cube import RubiksCube
import cubeUtils
import time

class DistancePieces:
    def __init__(self):
        self.memo_dist = dict()

        self.goal_cube = RubiksCube()
        self.goal_pieces = []

        self.goal_colors_positions = dict()
        self.goal_positions_colors = dict()

        self.all_positions = self.goal_cube.get_face_positions()

        for x, y, z in self.all_positions:
            colors = self.goal_cube.get_piece_colors(x, y, z)
            self.goal_pieces.append([x, y, z, colors])
            self.goal_positions_colors[str([x, y, z])] = colors

            colors_copy = colors.copy()
            colors_copy.sort()
            self.goal_colors_positions[str(colors_copy)] = [x, y, z]
        start = time.time()
        self._precalculate_individual_moves()
        end = time.time()
        print('Finish precalculation')
        print(f'Time of precalculation: {start-end}')
        
    def _precalculate_individual_moves(self):
        frontier = []
        
        cube = RubiksCube()

        for x, y, z, colors in self.goal_pieces:
            frontier.append([x, y, z, colors, 0])
            self.memo_dist[str([x, y, z, colors])] = 0

        while frontier:
            x, y, z, colors, dist = frontier.pop(0)

            movements = cubeUtils.get_all_movements()
            for mov in movements:
                cube.erase_piece(colors)
                cube.set_piece_colors(x, y, z, colors)
                cube.apply_movement(mov)

                x_next, y_next, z_next = cube.find_piece(colors)
                colors_next = cube.get_piece_colors(x_next, y_next, z_next)

                next_state = [x_next, y_next, z_next, colors_next]
                if str(next_state) not in self.memo_dist:
                    frontier.append([*next_state, dist + 1])
                    self.memo_dist[str(next_state)] = dist + 1

    def get_distance(self, x, y, z, colors):
        return self.memo_dist[str([x, y, z, colors])]
    
    def get_num_movements(self, cube):
        cost = 0
        for x, y, z in self.all_positions:
            colors = cube.get_piece_colors(x, y, z)
            dist = self.get_distance(x, y, z, colors)
            cost += dist
        return cost
    
    def get_manhattan_3D(self, cube):
        cost = 0
        positions = cube.get_face_positions()
        for x, y, z in positions:
            colors = cube.get_piece_colors(x, y, z)
            x_g, y_g, z_g = self.goal_cube.find_piece(colors)
            cost += abs(x_g-x)*(3-x)**2 + abs(y_g-y) + abs(z_g-z)
        return cost

if __name__ == '__main__':
    A = RubiksCube()
    scramble = cubeUtils.create_scramble()
    print(scramble)

    print(A)
    print(A.get_piece_colors(1, 2, 2))
    A.set_piece_colors(0, 0, 0, ['O', 'B', 'W'])
    print(A)
    A.apply_scramble(scramble)

    distance = DistancePieces()
    print(distance.get_distance(1, 2, 2, ['R', 'G']))
    print(distance.get_distance(1, 2, 2, ['G', 'R']))
#    print(A)
