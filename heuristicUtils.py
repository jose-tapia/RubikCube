from cube import RubiksCube
import cubeUtils

class DistancePieces:
    def __init__(self):
        self.memo = dict()

    def get_distance(self, x, y, z, colors):
        initial_state = [x, y, z, colors]
        if str(initial_state) in self.memo:
            return self.memo[str(initial_state)]
        
        cube = RubiksCube()

        x_f, y_f, z_f = cube.find_piece(colors)
        colors_f = cube.get_piece_colors(x_f, y_f, z_f)
        goal_state = [x_f, y_f, z_f, colors_f]
        
        frontier, explored = [], []
        frontier.append([x, y, z, colors, 0])
        while len(frontier) > 0:
            x, y, z, colors, dist = frontier.pop(0)

            current_state = [x, y, z, colors]
            
            if str(current_state) in explored:
                continue
            explored.append(str(current_state))

            print(current_state, dist)

            if str(current_state) == str(goal_state):
                self.memo[str(initial_state)] = dist
                return dist 

            movements = cubeUtils.get_all_movements()
            for mov in movements:
                cube.erase_piece(colors)
                cube.set_piece_colors(x, y, z, colors)
                cube.apply_movement(mov)

                x_next, y_next, z_next = cube.find_piece(colors)
                colors_next = cube.get_piece_colors(x_next, y_next, z_next)

                next_state = [x_next, y_next, z_next, colors_next]
                if str(next_state) is not explored:
                    frontier.append([*next_state, dist+1])
        return None

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
    print(distance.get_distance(1, 2, 2, ['R', 'G']))
#    print(A)
