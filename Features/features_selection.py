import csv
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import preprocessing
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./features.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
features = csvFile.drop(['quadrant'], axis=1)

# STANDARD DEVIATION  ***********************************************************************
std = features.std().sort_values()
counter = 0
to_drop = []
for feature in std.index:
    if std[feature] == 0:
        to_drop.append(feature)
df = features.drop(to_drop, axis=1)
# print(df)

df_correlation = df.corr().abs()
# https://www.dezyre.com/recipes/drop-out-highly-correlated-features-in-python
upper_tri = df_correlation.where(np.triu(np.ones(df_correlation.shape),k=1).astype(np.bool))

# IF CORRELATION = 1 ***********************************************************************
# correlation_equals_1 = [column for column in upper_tri.columns if any(upper_tri[column] == 1)]
# print(correlation_equals_1) 
# print('Number of features: ' + str(len(correlation_equals_1)))

# Find index of feature columns with correlation greater than 0.95 -
to_drop = []
to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)] # -1175
df1 = features.drop(to_drop, axis=1)
# print(df1) # features 2259

# df_correlation.to_csv('./features_correlation.csv', mode='w')

# PLOT ***********************************************************************
# fig, ax = plt.subplots(figsize=(24, 18))
# ax = sns.heatmap(df_correlation, annot = True, vmin=-1, vmax = 1, fmt='.2')
# ax.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
# add the column names as labels
# ax.set_yticklabels(df.columns, rotation = 0)
# ax.set_xticklabels(df.columns)
# plt.savefig('figure_huge.png', dpi=300)