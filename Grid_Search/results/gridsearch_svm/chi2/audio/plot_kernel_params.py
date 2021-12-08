import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# list of kernels to plot - poly, rbf, sigmoid
# list of datasets accompaniment, all combined, original, vocal, lyrics
path = '../lyrics/alljava_20210813'
file = 'best_sigmoid.csv'
csvFile = pd.read_csv(path + '/' + file, sep = ",", index_col=False)
unique_params = csvFile.drop_duplicates('params').copy() # drop rows where params are duplicated
params = list(unique_params['params'])
# e.g. ["{'C': 1, 'degree': 2, 'gamma': 'scale', 'kernel': 'poly'}", "{'C': 1, 'degree': 3, 'gamma': 'scale', 
# 'kernel': 'poly'}", "{'C': 10, 'degree': 3, 'gamma': 0.1, 'kernel': 'poly'}"]

for param in params:
    aux = csvFile.loc[csvFile['params'] == param].copy()
    plt.plot(aux['num_features'], aux['mean_test_score'], label=param)

plt.xlabel('Number of Features')
plt.ylabel('Mean Score - F1 macro')
plt.ylim(0.6, 0.67)
plt.legend(fontsize=8)
plt.title("Performance of the best params for sigmoid sigmoid - lyrics features (Chi2)", fontsize = 10)
plt.savefig(path + '/best_sigmoid_lyrics.png')

