import json
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time

from HeuristicUtils import Distances
from RubiksCube import RubiksCube 
import CubeUtils
import Search


def experiment(label, samples, heuristic):
    "Solve each sample with the given heuristic"

    times = []
    for idx, sample in enumerate(samples):
        cube = RubiksCube(sample)
        start_time = time.time()
        _ = Search.search(cube, heuristic)
        end_time = time.time()
        print(f'Experiment "{label}" : {idx} sample done')
        times.append(end_time - start_time)
    return times 

def group_experiments(group_heuristics, num_samples, scramble_size):
    "Solve the samples with each heuristic"

    samples = [CubeUtils.create_scramble(scramble_size) for _ in range(num_samples)]
    group_times = []
    for label, heuristic in group_heuristics:
        times = experiment(label, samples, heuristic)
        group_times.append(times)
    return group_times

def generate_experiment(num_samples, scramble_size, make_manhattan_heuristics = True, make_movements_heuristics = True, initial_range = 5, end_range = 13, folder_name = './Experiments'):
    "Given the settings, perform the experiment and store the times"

    np.random.seed(1)
    random.seed(10)

    distances = Distances()

    # Generate the different heuristics
    group_heuristics = []
    if make_manhattan_heuristics:
        for idx in range(initial_range, end_range):
            manhattan_idx = lambda cube: distances.get_manhattan_3D(cube) / idx
            group_heuristics.append([f'manhattan_{idx}', manhattan_idx])

    if make_movements_heuristics:
        for idx in range(initial_range, end_range):
            movements_idx = lambda cube: distances.get_movements_average(cube) / idx
            group_heuristics.append([f'movements_{idx}', movements_idx])

    # Make the test
    group_times = group_experiments(group_heuristics, num_samples, scramble_size)
    group_labels = [label for label, _ in group_heuristics]

    # Store and visualize the experiment
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    times_by_label = dict()
    for times, label in zip(group_times, group_labels):
        times_by_label[label] = times

    # Store experiment in a json    
    with open(f'{folder_name}/last_experiment_{num_samples}_{scramble_size}.json', 'w') as file:
        file.write(json.dumps(times_by_label, indent = 4))

    return group_labels, group_times

if __name__ == '__main__':
    folder_name = './Experiments'
    num_samples = 5
    scramble_size = 3

    group_labels, group_times = generate_experiment(num_samples, scramble_size, folder_name = folder_name)
    
    # Visualize with boxplots the reuslts
    fig = plt.figure(figsize = (18, 3))
    plt.boxplot(group_times)
    plt.xticks(range(1, len(group_labels) + 1), group_labels)

    plt.ylabel('Time')
    plt.xlabel('Constant')
    plt.savefig(f'{folder_name}/boxplot_figure_{num_samples}_{scramble_size}.svg', dpi = 333, transparent = True)
    plt.show()
