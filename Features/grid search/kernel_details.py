import pandas as pd
from os import listdir

kernel_list = ['rbf', 'poly', 'sigmoid'] # list of kernels
headers = ['num_features', 'kernel', 'params', 'rank_test_score', 'mean_test_score', 'std_test_score'] # headers for csv
best_kernels_csv = pd.DataFrame(columns=headers)

path = "./results_gridsearch_vocalaudio_20210813"
csvFile = pd.read_csv(path + '/best_kernels_csv_per_feature.csv', sep = ",", index_col=False)

for kernel in kernel_list:
    best_kernels_csv.to_csv(path + '/best_' + kernel + '.csv', index = False, columns=headers, mode='w')
    df = csvFile[csvFile['params'].str.contains(kernel)] # get all rows that have specific kernel in params
    df = df.drop_duplicates('params') # drop rows where params are duplicated
    params = list(df['params'])
    # df.to_csv(path + '/best_' + kernel + '.csv', header=False, index = False, mode='a')
    for file in listdir(path):
        dir = path + "/" + file
        if file.startswith("grid"):
            # for each file of features (10, 25, 50, ..., ) get rows of best params
            csv = pd.read_csv(dir, sep = ",", index_col=False)
            numFeatures = file.split('_')[3]

            df1 = csv.loc[csv['params'].isin(params)].copy()
            df1.insert(0, 'num_features', numFeatures) # add column num_features on left
            df1.to_csv(path + '/best_' + kernel + '.csv', header=False, index = False, mode='a')
    
    details = pd.read_csv(path + '/best_' + kernel + '.csv', sep = ",", index_col=False)
    details = details.sort_values(by = ['params', 'num_features'], ascending = True).copy()
    details.to_csv(path + '/best_' + kernel + '.csv', header=False, index = False, mode='w')

