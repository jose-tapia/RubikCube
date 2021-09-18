import json
import numpy as np
import os
import scipy.stats

from Experiments import generate_experiment



def ANOVA(group_times, significance_value = 0.05):
    """
        Manually perform an ANOVA test to check if the means of the experiments are equal or not
        
        - Null hypothesis: All the means are equal
        - Alternate hypothesis: Not all the means are equal
    """
    if len(group_times) <= 1:
        # The null hypothesis is true by emptiness
        return True
    
    # 1. Calculate means
    means = [np.mean(times) for times in group_times]

    all_times = [time for times in group_times for time in times]
    all_mean = np.mean(all_times)

    n = len(all_times)
    k = len(group_times)

    # 2. Sum of squares 

    ss_total = sum([(time - all_mean)**2 for time in all_times])
    ss_within = sum([sum([ (time - means[idx])**2 for time in group_times[idx]]) for idx in range(k)])
    ss_between = ss_total - ss_within

    # 3. Degrees of freedom
    df_within = k - 1
    df_between = n - k 

    # 4. Mean squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # 5. F statistic
    F = ms_between / ms_within

    # 6. F critical value 
    F_critical = scipy.stats.f.ppf(significance_value, df_between, df_within)

    # 7. Accept or reject null hypothesis
    return F < F_critical

def get_best_experiments(labels, group_times, significance_value = 0.05):
    "Using ANOVA test, determine which experiments has the best performance"
    means = [np.mean(times) for times in group_times]
    idx_sorted = list(range(len(labels)))
    idx_sorted.sort(key = lambda x : means[x])

    current_experiments_labels = []
    current_experiments_times = []
    for idx in idx_sorted:
        current_experiments_times.append(group_times[idx])
        if ANOVA(current_experiments_times, significance_value):
            current_experiments_labels.append(labels[idx])
        else:
            break
    return current_experiments_labels

if __name__ == '__main__':
    # Set experiment
    folder_name = './Experiments'
    num_samples = 7
    size_scramble = 2

    experiments = dict()
    # Get experiment information
    if not os.path.isfile(f'{folder_name}/last_experiment_{num_samples}_{size_scramble}.json'):
        print('Experiment does not exists yet, creating experiment...')
        group_labels, group_times = generate_experiment(num_samples, size_scramble, folder_name = folder_name)

        experiments = dict()
        for times, label in zip(group_times, group_labels):
            experiments[label] = times
    else:
        with open(f'{folder_name}/last_experiment_{num_samples}_{size_scramble}.json', 'r') as file:
            experiments = json.loads(file.read())

    # Split experiments according to the heuristic
    manhattan = 'manhattan'
    movements = 'movements'
    
    labels_manhattan = []
    group_times_manhattan = []
    
    labels_movements = []
    group_times_movements = []

    for experiment in experiments:
        if experiment[:len(manhattan)] == manhattan:
            labels_manhattan.append(experiment)
            group_times_manhattan.append(experiments[experiment])
            print(experiment)
        elif experiment[:len(movements)] == movements:
            labels_movements.append(experiment)
            group_times_movements.append(experiments[experiment])
            print(experiment)
    
    # Obtain the best constants according to the groups
    print(get_best_experiments(labels_manhattan, group_times_manhattan, 0.001))
    print(get_best_experiments(labels_movements, group_times_movements, 0.001))
