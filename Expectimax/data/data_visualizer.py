import pickle
import matplotlib.pyplot as plt
import numpy as np

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
        averages.append(data[str(i)][3])
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

print(full_data_set['weighted_fill']['1'][3])

print(full_data_set['simple_fill']['1'][3])
print(full_data_set['max_fill']['1'][3])



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
    width = .1
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
            name = method + '_fill'
            plot = ax.bar(np.arange(num_boards) + i * width, averages[name], width, label=method+"_fill")
            all_plots.append(plot)
            names.append(name)
            #autolabel(plot)
        else:
            name = method + '_sample'
            plot = ax.bar(np.arange(num_boards) + i * width, averages[method + '_sample'], width, label=method+"_sample")
            all_plots.append(plot)
            names.append(name)
            #autolabel(plot)

    ax.set_xticklabels([0]+ALL_BOARDS)
    ax.legend(all_plots, names)
    plt.show()

plot_data(1)



