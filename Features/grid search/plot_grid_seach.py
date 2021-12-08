import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# kernel_list = ['rbf', 'linear', 'poly', 'sigmoid'] # list of kernels

# path = './results_gridsearch_vocalaudio_20210813/best_kernels_csv_per_feature.csv'

# csvFile = pd.read_csv(path, sep = ",", index_col=False)
# for kernel in kernel_list:
#     aux = csvFile[csvFile['params'].str.contains(kernel)] # rows that have the specific kernel name in params column
#     plt.plot(aux['num_features'], aux['mean_test_score'], label=kernel)

# plt.xlabel('Number of Features')
# plt.ylabel('Mean Score')
# plt.legend()
# plt.title("Kernels performance on Grid search - vocal features")
# plt.savefig('grid_search_vocal_audio.png')

# RBF
# read csv file with features
csvFile = pd.read_csv('./Livro1.csv', sep = ";", index_col=False)
# path = './results_gridsearch_vocalaudio_20210813/best_kernels_csv_per_feature.csv'

# PLOT
# fig = plt.figure(figsize=(10,5))
# PLOTS -------
i = 0
while i < len(csvFile):
    aux = csvFile.iloc[i:i+12,:].copy()
    plt.plot(aux['Features'], aux['mean'], label=aux['params'].iloc[[0]].to_string(index=False))
    i = i + 12
# -------------
plt.ylim(0.54, 0.7)
plt.xlabel('Number of Features')
plt.ylabel('Mean Score')
plt.legend(fontsize=9)

plt.savefig('kernel_rbf.png')
