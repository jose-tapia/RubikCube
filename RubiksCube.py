import CubeUtils

basic_movements = CubeUtils.get_basic_movements()

class RubiksCube:
    def __init__(self, scramble = []):
        #we initialize the attribute, referring to the object itself, also have a input of how the scramble its going. 
        self.faces = [[[color for _ in range(3)] for _ in range(3) ] for color in CubeUtils.colors]

        self.apply_scramble(scramble)
    
    def __eq__(self, other):
        if other is None:
            return False
        # Check array of faces to verify if two cubes are equal
        return self.faces == other.faces
    
    def __str__(self):
        # Empty face
        empty = [[' ']*3]*3

        # Print faces with the following pattern 
        #   W
        # O G R B
        #   Y
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
        "Apply movement to the cube"
        basic_movement = CubeUtils.get_movement_prefix(movement)
        suffix_movement = CubeUtils.get_movement_suffix(movement)

        # Verify if the movement is valid
        if basic_movement not in basic_movements:
            return 
        
        # Get settings for movement
        face, face_dir, row, column, line_dir = CubeUtils.cube_movements[basic_movement]

        # Apply suffix changes to settings
        if suffix_movement == '2':
            face_dir = 'U'
            line_dir = 'U'
        elif suffix_movement == "'":
            face_dir = 'L' if face_dir == 'R' else 'R'
            line_dir = 'L' if line_dir == 'R' else 'R'

        # Rotate face and respective line
        self._rotate_matrix(self.faces[face], dir = face_dir)
        self._rotate_lines(row = row, column = column, dir = line_dir)

    def apply_scramble(self, scramble):
        "Apply scramble to the cube"
        for movement in scramble:
            self.apply_movement(movement)

    def set_piece(self, piece, colors):
        "Given the piece's positions and the color list, set it in the cube"
        if len(piece) != len(colors):
            return 
        for (face, x, y), color in zip(piece, colors):
            self.faces[face][x][y] = color
    
    def get_colors(self, piece):
        "Obtain colors for a given piece"
        colors = []
        for face, x, y in piece:
            colors.append(self.faces[face][x][y])
        return colors

    def erase_piece(self, piece):
        "Erase colors for a given piece"
        if piece is None:
            return
        for face, x, y in piece:
            self.faces[face][x][y] = 'X'

    def find_piece(self, colors):
        "Find piece with such combination of colors"
        colors_copy = colors.copy()
        colors_copy.sort()
        for piece in CubeUtils.cube_pieces_positions:
            color_piece = []
            for face, x, y in piece:
                color_piece.append(self.faces[face][x][y])
            color_piece.sort()
            if colors_copy == color_piece:
                return piece
        return None

    @staticmethod
    def _rotate_matrix(matrix, dir = ''):
        "Rotate a matrix depending the direction indicated"
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
        "Rotate the line indicated"
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

    # Test get colors method    
    print(cube)
    for piece in CubeUtils.cube_pieces_positions:
        colors = cube.get_colors(piece)
        colorines = ''.join(colors)
        print(f'Piece : {colorines}')

    # Test apply movement method
    cube = RubiksCube()
    cube.apply_movement('L')
    print(cube)
    cube.apply_movement('L')
    print(cube)
    cube.apply_movement('L')
    print(cube)
    cube.apply_movement('L')

    # Test find and erase piece method
    A = cube.find_piece(['Y', 'O', 'B'])
    print(A)
    cube.apply_movement("B2")
    print(cube)
    cube.erase_piece(A)
    print(cube)
    cube.set_piece(A, ['1', '2', '3'])
    print(cube)