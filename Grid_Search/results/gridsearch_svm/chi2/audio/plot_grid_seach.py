import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

kernel_list = ['rbf', 'linear', 'poly', 'sigmoid'] # list of kernels

path = '../lyrics/alljava_20210813/'

ymax = 0
csvFile = pd.read_csv(path + "best_kernels_csv_per_feature.csv", sep = ",", index_col=False)
for kernel in kernel_list:
    aux = csvFile[csvFile['params'].str.contains(kernel)] # rows that have the specific kernel name in params column
    plt.plot(aux['num_features'], aux['mean_test_score'], label=kernel)
    if max(aux['mean_test_score']) > ymax:
        ymax = max(aux['mean_test_score'])
        xpos = list(aux['mean_test_score']).index(ymax)
        xmax = list(aux['num_features'])[xpos]


plt.annotate("{:.5f}".format(ymax), xy=(xmax, ymax), xytext=(xmax-3, ymax+0.008), 
arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),horizontalalignment='center', verticalalignment='top')

plt.ylim(0.6,0.67)
plt.xlabel('Number of Features')
plt.ylabel('Mean Score - F1 macro')
plt.legend()
plt.title("Kernels performance on Grid search - lyrics features (Chi2)")
plt.savefig(path + 'grid_search_lyrics.png')