import numpy as np

colors = ['W', 'O', 'G', 'R', 'B', 'Y']

orientation = dict({'U':[0, None, None], 
                    'W':[None, None, 0], 
                    'S':[None, 2, None], 
                    'E':[None, None, 2],  
                    'N':[None, 0, None],
                    'D':[2, None, None],
                    '':[None, None, None]})

cube_notations = dict({'U': ['U', -np.pi/2, 0, 0], 
                       'L': ['W', 0, 0, -np.pi/2],
                       'F': ['S', 0, np.pi/2, 0],
                       'R': ['E', 0, 0, np.pi/2],
                       'B': ['N', 0, -np.pi/2, 0],
                       'D': ['D', np.pi/2, 0, 0]})
        
cube_dirs = [[[[] for _ in range(3)] for _ in range(3) ] for _ in range(3)]
        
def get_rotation_matrix(alpha, beta, gamma):
    Rx = [[1, 0, 0], 
            [0, np.cos(alpha), -np.sin(alpha)],
            [0, np.sin(alpha), np.cos(alpha)]]
    Ry = [[np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]]
    Rz = [[np.cos(gamma), -np.sin(gamma), 0],
            [np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 1]]
    return np.matmul(np.matmul(Rx, Ry), Rz)