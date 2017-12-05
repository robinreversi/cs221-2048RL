import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import operator

import math

sns.set()
sns.set_style("white")
sns.set_context("talk")
sns.set_palette(sns.color_palette(["blue", "orange", "orangered", "lightgreen"]))




ALL_BOARDS = [1, 2, 3, 4, 5, 10, 50]
METHODS = ['direness', 'simple', 'weighted', 'max']


def load_data(method, fill):
    '''
    loads data for one method / fill combo
    '''
    boards_to_data = {}
    for i in ALL_BOARDS:
        #if(not (method == 'simple' and i == 100 or method == 'weighted' and i == 100)):
        filename = "d" + str(2) + "b" + str(i) + "g" + str(30) + "f" + str(fill) + "m" + method
        with open(filename, "rb") as f:
            boards_to_data[str(i)] = pickle.load(f)

    return boards_to_data

def make_full_data_set():
    full_data_set = {}
    for method in METHODS:
        fill_key = method + "_fill"
        sample_key = method + "_sample"
        full_data_set[fill_key] = load_data(method, 1)
        full_data_set[sample_key] = load_data(method, 0)

    return full_data_set

def get_acc_data(data):
    averages = []
    for i in ALL_BOARDS:
        averages.append(math.log(data[str(i)][3]))
    return averages


'''
0 - all scores
1 - map of lowest highest tiles across all boards
2 - map of highest tiles across all boards
3 - average
4 - variance

ex call: full_data_set['method_fill']['board num'][3]

full
-> strategy
-> -> number of boards as string
-> -> -> data for that # of boards

'''

full_data_set = make_full_data_set()

def plot_data(fill):
    averages = {}
    for method in METHODS:
        if(fill):
            fill = get_acc_data(full_data_set[method + "_fill"])
            averages[method + '_fill'] = fill
        else:
            sample = get_acc_data(full_data_set[method + "_sample"])
            averages[method + '_sample'] = sample
    
    fig, ax = plt.subplots()
    width = .15
    num_boards = len(ALL_BOARDS)

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    all_plots = []
    names = []

    for i, method in enumerate(METHODS):
        if(fill):
            plot = ax.bar(np.arange(num_boards) + i * width, averages[method + '_fill'], width, label=method)
            all_plots.append(plot)
            names.append(method)
            #autolabel(plot)
        else:
            plot = ax.bar(np.arange(num_boards) + i * width, averages[method + '_sample'], width, label=method)
            all_plots.append(plot)
            names.append(method)
            #autolabel(plot)

    ax.set_xticklabels([0]+ALL_BOARDS)
    ax.legend(all_plots, names)
    word = "Fill" if fill else "Sample"
    title = "Log-Score vs Number of Boards using " + word + " Estimate"
    ax.set_title(title)
    ax.set_ylim(ymin=5.5)
    ax.set_ylabel('Log-Score')
    ax.set_xlabel('Number of Boards')


    plt.show()

plot_data(1)
#plot_data(0)

def table_data(fill):
    key_word = 'fill' if fill else 'sample'
    table = []
    for method in METHODS:
        method_data = full_data_set[method + '_' + key_word]
        maxs = []
        maxs.append(method)
        for i in ALL_BOARDS:
            max_values = method_data[str(i)][2]
            maxs.append(max(max_values.items(), key=operator.itemgetter(0))[0])
        table.append(maxs)
    table = pd.DataFrame(table, columns=['method'] + ALL_BOARDS)
    table.to_csv(key_word + '.csv')


#table_data(1)
#table_data(0)



