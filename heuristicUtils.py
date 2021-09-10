from cube import RubiksCube
import cubeUtils

if __name__ == '__main__':
    A = RubiksCube()
    scramble = cubeUtils.create_scramble()
    print(scramble)

    print(A)
    A.apply_scramble(scramble)
    print(A)