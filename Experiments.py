from HeuristicUtils import Distances
import Search
from RubiksCube import RubiksCube 
import CubeUtils
import time
import matplotlib.pyplot as plt
from heapq import heappop, heappush
import random
import json
import numpy as np

def experiment(samples, settings):
    times = []
    for idx, sample in enumerate(samples):
        cube = RubiksCube(sample)
        start_time = time.time()
        _ = Search.search(cube, settings)
        end_time = time.time()
        print(f'Experiment "{settings["name"]}" : {idx} sample done')
        times.append(end_time - start_time)
    return times 

def group_experiments(group_settings, num_samples = 50, size_scramble = 8):
    samples = [CubeUtils.create_scramble()[:size_scramble] for _ in range(num_samples)]
    group_times = []
    for settings in group_settings:
        times = experiment(samples, settings)
        group_times.append(times)
    return group_times

if __name__ == '__main__':
    np.random.seed(1)
    random.seed(100)

    distances = Distances()

    push_state_heap = lambda node, frontier: heappush(frontier, node)
    pop_state_heap = lambda frontier: heappop(frontier)

    group_settings = []
    for idx in range(4, 10):
        settings = dict({
            'name' : f'manhattan_{idx}',
            'push_state' : push_state_heap,
            'pop_state' : pop_state_heap,
            'cost_function' : lambda cube, cost: cost + distances.get_manhattan_3D(cube) / idx
        })
        group_settings.append(settings)
        
        settings = dict({
            'name' : f'movements_{idx}',
            'push_state' : push_state_heap,
            'pop_state' : pop_state_heap,
            'cost_function' : lambda cube, cost: cost + distances.get_movements_average(cube) / idx
        })
        group_settings.append(settings)
    
    group_times = group_experiments(group_settings, num_samples = 20, size_scramble = 8)
    group_names = [settings['name'] for settings in group_settings]



    folder_name = './Experiments/'

    times_by_name = dict()
    for times, name in zip(group_times, group_names):
        times_by_name[name] = times
    
    with open(folder_name + 'last_experiment.json', 'w') as file:
        file.write(json.dumps(times_by_name, indent = 4))


    fig = plt.figure(figsize = (16, 3))
    plt.boxplot(group_times)
    plt.xticks(range(1, len(group_names) + 1), group_names)

    plt.ylabel('Time')
    plt.xlabel('Constant')
    plt.savefig(folder_name + 'boxplot_figure.svg', dpi = 333, transparent = True)
    plt.show()

