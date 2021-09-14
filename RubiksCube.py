import cubeUtils

class RubiksCube:
    def __init__(self, scramble = []):
        self.faces = [[[f'{a+3*b}{color}' for a in range(3)] for b in range(3) ] for color in cubeUtils.colors]

        self._basic_movements = cubeUtils.get_basic_movements()
        self._all_movements = cubeUtils.get_all_movements()

        for movement in scramble:
            self.apply_movement(movement)
    
    def __str__(self):
        empty = [['  ']*3]*3
        first_line = [empty, self.faces[0]]
        second_line = self.faces[1:5]
        third_line = [empty, self.faces[5]]

        cube_str = ['']
        for line in [first_line, second_line, third_line]:
            for subline in range(3):
                for face in line:
                    for c in face[subline]:
                        cube_str.append(str(c))
                    cube_str.append(' ')
                cube_str.append('\n')
        return ' '.join(cube_str)

    def apply_movement(self, movement):
        basic_movement = cubeUtils.get_movement_prefix(movement)
        suffix_movement = cubeUtils.get_movement_suffix(movement)
        if basic_movement not in self._basic_movements:
            return 
        
        face, face_dir, row, column, line_dir = cubeUtils.cube_movements[basic_movement]

        if suffix_movement == "'":
            face_dir = 'L' if face_dir == 'R' else 'R'
            line_dir = 'L' if line_dir == 'R' else 'R'
        elif suffix_movement == '2':
            face_dir = 'U'
            line_dir = 'U'

        self._rotate_matrix(self.faces[face], dir = face_dir)
        self._rotate_lines(row = row, column = column, dir = line_dir)

        return
        """
        if basic_movement == 'U':
            self._rotate_matrix(self.faces[0], dir = 'L')
            self._rotate_lines(row = 0, dir = 'L')
        elif basic_movement == 'D':
            self._rotate_matrix(self.faces[5], dir = 'L')
            self._rotate_lines(row = 2, dir = 'R')
        elif basic_movement == 'L':
            self._rotate_matrix(self.faces[1], dir = 'L')
            self._rotate_lines(column = 3, dir = 'L')
        elif basic_movement == 'R':
            self._rotate_matrix(self.faces[3], dir = 'L')
            self._rotate_lines(column = 5, dir = 'R')
        elif basic_movement == 'F':
            self._rotate_matrix(self.faces[2], dir = 'L')
            self._rotate_lines(column = 2, dir = 'R')
        elif basic_movement == 'B':
            self._rotate_matrix(self.faces[4], dir = 'L')
            self._rotate_lines(column = 0, dir = 'L')
        """
    
    @staticmethod
    def _rotate_matrix(matrix, dir = ''):
        if dir == '':
            return
        elif dir == 'R':
            matrix[0][0], matrix[0][2], matrix[2][2], matrix[2][0] = matrix[0][2], matrix[2][2], matrix[2][0], matrix[0][0]
            matrix[0][1], matrix[1][2], matrix[2][1], matrix[1][0] = matrix[1][2], matrix[2][1], matrix[1][0], matrix[0][1]
        elif dir == 'L':
            matrix[0][0], matrix[0][2], matrix[2][2], matrix[2][0] = matrix[2][0], matrix[0][0], matrix[0][2], matrix[2][2]
            matrix[0][1], matrix[1][2], matrix[2][1], matrix[1][0] = matrix[1][0], matrix[0][1], matrix[1][2], matrix[2][1]
        elif dir == 'U':
            matrix[0][0], matrix[2][2] = matrix[2][2], matrix[0][0]
            matrix[0][1], matrix[2][1] = matrix[2][1], matrix[0][1]
            matrix[0][2], matrix[2][0] = matrix[2][0], matrix[0][2]
            matrix[1][0], matrix[1][2] = matrix[1][2], matrix[1][0]     
    
    def _rotate_lines(self, row = None, column = None, dir = ''):
        if row is not None and column is not None: 
            return 
        elif row is not None:
            if row == 1 or dir == '':
                return
            elif dir == 'L':        
                self.faces[1][row], self.faces[2][row], self.faces[3][row], self.faces[4][row] = self.faces[2][row], self.faces[3][row], self.faces[4][row], self.faces[1][row]
            elif dir == 'R':        
                self.faces[1][row], self.faces[2][row], self.faces[3][row], self.faces[4][row] = self.faces[4][row], self.faces[1][row], self.faces[2][row], self.faces[3][row]
            elif dir == 'U':
                self.faces[1][row], self.faces[2][row], self.faces[3][row], self.faces[4][row] = self.faces[3][row], self.faces[4][row], self.faces[1][row], self.faces[2][row]
        elif column is not None:
            if column == 1 or column == 4 or column >= 6 or dir == '':
                return
            elif dir == 'L':
                if column < 3:
                    first_column = [self.faces[1][row][column] for row in range(3)]
                    for row in range(3):
                        self.faces[1][row][column] = self.faces[0][column][2-row]
                        self.faces[0][column][2-row] = self.faces[3][2-row][2-column]
                        self.faces[3][2-row][2-column] = self.faces[5][2-column][row]
                        self.faces[5][2-column][row] = first_column[row]
                elif column < 6:
                    column -= 3
                    first_column = [self.faces[2][row][column] for row in range(3)]
                    for row in range(3):
                        self.faces[2][row][column] = self.faces[0][row][column]
                        self.faces[0][row][column] = self.faces[4][2-row][2-column]
                        self.faces[4][2-row][2-column] = self.faces[5][row][column]
                        self.faces[5][row][column] = first_column[row]
            elif dir == 'R':
                if column < 3:
                    first_column = [self.faces[1][row][column] for row in range(3)]
                    for row in range(3):
                        self.faces[1][row][column] = self.faces[5][2-column][row]
                        self.faces[5][2-column][row] = self.faces[3][2-row][2-column] 
                        self.faces[3][2-row][2-column] = self.faces[0][column][2-row]
                        self.faces[0][column][2-row] = first_column[row]
                elif column < 6:
                    column -= 3
                    first_column = [self.faces[2][row][column] for row in range(3)]
                    for row in range(3):
                        self.faces[2][row][column] = self.faces[5][row][column]
                        self.faces[5][row][column] = self.faces[4][2-row][2-column]
                        self.faces[4][2-row][2-column] = self.faces[0][row][column]
                        self.faces[0][row][column] = first_column[row]
            elif dir == 'U':
                if column < 3:
                    for row in range(3):
                        self.faces[1][row][column], self.faces[3][2-row][2-column] = self.faces[3][2-row][2-column], self.faces[1][row][column]
                        self.faces[0][column][2-row], self.faces[5][2-column][row] = self.faces[5][2-column][row], self.faces[0][column][2-row]
                elif column < 6:
                    column -= 3
                    for row in range(3):
                        self.faces[2][row][column], self.faces[4][2-row][2-column] = self.faces[4][2-row][2-column], self.faces[2][row][column]
                        self.faces[0][row][column], self.faces[5][row][column] = self.faces[5][row][column], self.faces[0][row][column]
                       

if __name__ == '__main__':
    cube = RubiksCube()
    print(cube)
    cube.apply_movement("B2")
    print(cube)
#    cube.apply_basic_movement('L')
 #   print(cube)
  #  cube.apply_basic_movement('L')
   # print(cube)
    #cube.apply_basic_movement('L')
    #print(cube)
    pass