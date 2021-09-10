import numpy as np
from copy import deepcopy

orientation = dict({'U':[0, None, None], 
                    'N':[None, 0, None], 
                    'E':[None, None, 2], 
                    'S':[None, 2, None], 
                    'W':[None, None, 0], 
                    'D':[2, None, None],
                    '':[None, None, None]})

cube_notations = dict({'U': ['U', -np.pi/2, 0, 0],
                       'B': ['N', 0, -np.pi/2, 0],
                       'R': ['E', 0, 0, np.pi/2],
                       'F': ['S', 0, np.pi/2, 0], 
                       'L': ['W', 0, 0, -np.pi/2],
                       'D': ['D', np.pi/2, 0, 0]})

class Cube:
    def __init__(self):
        self.cube = [[['X' for _ in range(3)] for _ in range(3)] for _ in range(3)]
    
    def __str__(self):
        empty = [[' ']*3]*3
        first_line = [empty, self.get_face('U')]
        second_line = [self.get_face('W'), self.get_face('S'), self.get_face('E'), self.get_face('N')]
        third_line = [empty, self.get_face('D')]

        cube_str = ['']
        for line in [first_line, second_line, third_line]:
            for subline in range(3):
                for face in line:
                    for c in face[subline]:
                        cube_str.append(str(c))
                    cube_str.append(' ')
                cube_str.append('\n')
        return ' '.join(cube_str)

    def get_face_positions(self, dir = ''):    
        x_default, y_default, z_default = orientation[dir]
        xs = [x_default] if x_default is not None else range(len(self.cube))
        ys = [y_default] if y_default is not None else range(len(self.cube[0]))
        zs = [z_default] if z_default is not None else range(len(self.cube[0][0]))
        return [[x, y, z] for x in xs for y in ys for z in zs]

    def get_face(self, dir):
        if dir != '':
            positions = self.get_face_positions(dir)
            colors = [self.cube[x][y][z] for x, y, z in positions]
            return [colors[:3], colors[3:6], colors[6:]]   
        else:
            return []

    def set_color(self, dir, color):
        face = self.get_face_positions(dir)
        for x, y, z in face:
            self.cube[x][y][z] = color

    def get_color(self, dir):
        x, y, z = orientation[dir]
        x = x if x is not None else 1
        y = y if y is not None else 1
        z = z if z is not None else 1
        return self.cube[x][y][z]
    
    def apply_rotation(self, alpha, beta, gamma, face = ''):
        Rx = [[1, 0, 0], 
              [0, np.cos(alpha), -np.sin(alpha)],
              [0, np.sin(alpha), np.cos(alpha)]]
        Ry = [[np.cos(beta), 0, np.sin(beta)],
              [0, 1, 0],
              [-np.sin(beta), 0, np.cos(beta)]]
        Rz = [[np.cos(gamma), -np.sin(gamma), 0],
              [np.sin(gamma), np.cos(gamma), 0],
              [0, 0, 1]]
        R = np.matmul(np.matmul(Rx, Ry), Rz)

        positions = self.get_face_positions(face)
        cube = deepcopy(self.cube)
        for x, y, z in positions:
            x_r, y_r, z_r = np.matmul(R, [x-1, y-1, z-1])
            x_r, y_r, z_r = int(np.rint(x_r+1)), int(np.rint(y_r+1)), int(np.rint(z_r+1))
            self.cube[x_r][y_r][z_r] = cube[x][y][z]

class RubiksCube(Cube):
    def __init__(self, scramble = []):
        self.cube = [[[Cube() for _ in range(3)] for _ in range(3)] for _ in range(3)]

        colors = ['W', 'O', 'G', 'R', 'B', 'Y']
        dirs = ['U', 'W', 'S', 'E', 'N', 'D']
        for dir, color in zip(dirs, colors):
            positions = self.get_face_positions(dir)
            for x, y, z in positions:
                self.cube[x][y][z].set_color(dir, color)
        
        self._apply_scramble(scramble)
    
    def get_face(self, dir):
        if dir != '':
            positions = self.get_face_positions(dir)
            colors = [self.cube[x][y][z].get_color(dir) for x, y, z in positions]
            if dir in ['U', 'S', 'W']:
                return [colors[:3], colors[3:6], colors[6:]]   
            if dir in ['N', 'E']:
                color_matrix = [colors[:3], colors[3:6], colors[6:]]
                for idx in range(3):
                    color_matrix[idx].reverse()
                return color_matrix
            if dir == 'D':
                return [colors[6:], colors[3:6], colors[:3]]
        return []
    
    def _apply_basic_movement(self, movement):
        dir, alpha, beta, gamma = cube_notations[movement]

        self.apply_rotation(alpha, beta, gamma, dir)
        positions = self.get_face_positions(dir)
        for x, y, z in positions:
            self.cube[x][y][z].apply_rotation(alpha, beta, gamma)

    def apply_movement(self, movement):
        if movement in cube_notations:
            self._apply_basic_movement(movement)
            return
        
        if len(movement) == 2 and movement[0] in cube_notations and movement[1] in ["'", '2']:
            self._apply_basic_movement(movement[0])
            self._apply_basic_movement(movement[0])
            if movement[1] == '2':
                return
            self._apply_basic_movement(movement[0])
            return
        else:
            print('Unsupported movement')
            return


    def _apply_scramble(self, scramble):
        for movement in scramble:
            self.apply_movement(movement)

if __name__ == "__main__":
    #rubik_1 = RubiksCube(["D'", "R", "L", "F", "R'", "L", "U2", "F", "D2", "R'", "L2", "F2", "D", "R2", "B2", "D2", "L2", "U'", "B2", "U'"])
    #rubik_2 = RubiksCube(["F", "R2", "U'"])
    rubik_3 = RubiksCube(["B", "F", "U", "L'", "D'", "R'","F'"])
    rubik_4 = RubiksCube(["U'", "F", "B", "R'", "U", "R'", "F'", "D2", "L", "F", "U'", "F2", "L2", "U'", "D", "L2", "U'", "B2", "U'"])

    #print(rubik_1)
    #print(rubik_2)
    print(rubik_4)