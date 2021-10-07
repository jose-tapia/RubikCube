# Rubik's Cube

## Context
The Rubik's Cube is a 3-D combination puzzle invented in 1971 by Hungarian sculptor and professor of architecture Ernő Rubik. The six faces are covered by nine stickers, each one of six solid colors: white, red, blue, orange, green, and yellow. An internal pivot mechanism enables each face to turn independently, thus mixing up the colors. 
For the puzzle to be solved, each face must be returned to have only one color. 

## Contribution

The Rubik's cube is represented as a list of six arrays of 3x3, representing each one of the six faces. 

This implementation support the following movements:
  - The basic movements
    - F (Front, clockwise direction)
    - B (Back, clockwise direction)
    - U (Up, clockwise direction)
    - D (Down, clockwise direction)
    - L (Left, clockwise direction)
    - R (Right, clockwise direction)
  - The inverse movements of the basic ones
    - F' (Front, anticlockwise direction)
    - B' (Back, anticlockwise direction)
    - U' (Up, anticlockwise direction)
    - D' (Down, anticlockwise direction)
    - L' (Left, anticlockwise direction)
    - R' (Right, anticlockwise direction)
  - And their 180-degree turn versions
    - F2 (Front, two turns)
    - B2 (Back, two turns)
    - U2 (Up, two turns)
    - D2 (Down, two turns)
    - L2 (Left, two turns)
    - R2 (Right, two turns)

Giving a total of 18 movements. Nevertheless, the factor branch of the search is reduced to 12 thanks to clever observations that avoid repeat states. 

The implementation of the Rubik's cube state can be found in [RubiksCube.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/RubiksCube.py).

### Search
We implemented an A* algorithm to search for a solution for a scrambled Rubik's cube; The algorithm is refactored to easily choose the heuristic that would be used in the search. 

The implementation of the search can be found in [Search.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/Search.py).

### Heuristics

The heuristics considered in this project are:
 - Sum the number of movements that each piece would do to optimally reach its position in the goal state (solved Rubik's cube). 
   - To don't overestimate the true cost of the solution, this number is divided by a fixed number, it used to be 4 or 5.
 - Sum of the manhattan distances from each piece to its position in the goal state, looking at each piece in its respective tridimensional cartesian coordinates.
   - To don't overestimate the true cost of the solution, this number is divided by a fixed number, it used to be 8-9.

The implementation of the mentioned heuristics can be found in [HeuristicUtils.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/HeuristicUtils.py).

### Experiments and statistics

To determine which constant could be a good option as a divisor to don't overestimate the cost of the solution, few functions were implemented in [Experiments.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/Experiments.py) and analyzed in [Statistics.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/Statistics.py) using an ANOVA test. 

As well, in the folder Experiments, the results of the experiments can be found.

### Further improvements
As attempts to improve the results obtained by the project, the following ideas can be considered:
 - Implement a bidirectional search (See [BidirectionalSearch.py](https://github.com/jose-tapia/RubiksCube/blob/b77101bfaa9983418a67cede168e5c5781d9dcfe/BidirectionalSearch.py) for two attempts of this idea)
 - Include different heuristics
 - Include precalculated data to have a more precise estimation of the cost for the heuristic
 - One idea implemented was to use the tridimensional coordinates space to represent the Rubik's cube, it was discarded as the movements were very slow (Found in [Geometry_3D](https://github.com/jose-tapia/RubiksCube/tree/main/Geometry_3D) folder)
 - Include a graphic way to interact with the user to ask for the scramble of the Rubik's cube and show the solution found by the program

## Results of the project
The current implementation can solve in less than 1-2 seconds Rubik's cubes scrambled with less or equal to 5 movements. 

For almost all the cases, in less than a minute a Rubik's cubes scrambled with less or equal to 8 movements are solved.

## Team members
 - José Manuel Tapia Avitia A00834191
 - Pablo César Ruíz Hernández A01197044
 - Carlos Alonzo López Castañeda A01378902
