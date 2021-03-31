import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./features_without_null.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)

# features_accompaniment = features.iloc[:,0:4034].copy()
# features_original = features.iloc[:,4034:(8068)].copy()
# features_vocals = features.iloc[:,8068:].copy()

#   ******************** VARIANCE ***************************************************
var = csvFile.var().sort_values()
to_drop = []
for feature in var.index:
    if var[feature] == 0:
        to_drop.append(feature)
csvFile = csvFile.drop(to_drop, axis=1)
# print(len(to_drop)) # DROP 1760

# df_correlation = csvFile.corr().abs()

# # https://www.dezyre.com/recipes/drop-out-highly-correlated-features-in-python
# upper_tri = df_correlation.where(np.triu(np.ones(df_correlation.shape),k=1).astype(np.bool))

# # Find index of feature columns with correlation greater than 0.95 -
# to_drop = []
# to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)] # -1175
# df1 = features.drop(to_drop, axis=1)
# print(df1) # features 2259

# df_correlation.to_csv('./features_correlation.csv', mode='w')

# ***********************************PLOTS*******************************
# ****************************HEATMAP****************************
# fig, ax = plt.subplots(figsize=(24, 18))
# ax = sns.heatmap(df_correlation, annot = True, vmin=-1, vmax = 1, fmt='.2')
# ax.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
# add the column names as labels
# ax.set_yticklabels(df.columns, rotation = 0)
# ax.set_xticklabels(df.columns)
# plt.savefig('figure_huge.png', dpi=300)