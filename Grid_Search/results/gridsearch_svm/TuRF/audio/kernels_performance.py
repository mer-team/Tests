import pandas as pd
from os import listdir

kernel_list = ['rbf', 'linear', 'poly', 'sigmoid'] # list of kernels
headers = ['num_features', 'kernel', 'params', 'rank_test_score', 'mean_test_score', 'std_test_score'] # headers for csv
path = "./accompaniment_20210813/"
best_kernels_csv = pd.DataFrame(columns=headers)
best_kernels_csv.to_csv(path + 'best_kernels_csv_per_feature.csv', index = False, columns=headers, mode='w')

for file in listdir(path):
    if file.startswith("grid"):

        dir = path + file
        # read csv file
        csvFile = pd.read_csv(dir, sep = ",", index_col=False)
        numFeatures = pd.DataFrame({ 'num_features':[file.split('_')[3]]})

        for kernel in kernel_list:
            # get all rows that have specific kernel in params. Then we get only first one because its sorted by score
            df = csvFile[csvFile['params'].str.contains(kernel)].head(1)
            df.reset_index(drop=True, inplace=True)
            best_kernel = pd.concat([numFeatures, df], axis = 1)
            best_kernel.to_csv(path + 'best_kernels_csv_per_feature.csv', header=False, index = False, mode='a')
