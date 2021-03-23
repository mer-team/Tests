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

# NAN AND INF **************************************
features_null = features.isnull().sum().sort_values(ascending = False) # check number of NAN values per column | max registered was 18
# features_null.to_csv('./features_null.csv', mode='w')
# PLOT NAN **************
# values = []
# index_plot = []
# counter = 1
# for feat in features_null.index:
#     values.append(features_null[feat])
#     index_plot.append(feat)
#     if features_null[feat] == 0:
#         break
#     counter += 1
# x = np.arange(len(index_plot))  # the label locations
# width = 0.5  # the width of the bars
# fig, ax = plt.subplots()

# bars = ax.bar(x, values, width)

# ax.set_ylabel('Number of NAN')
# ax.set_xlabel('Features')
# ax.set_xticks(x)
# ax.set_xticklabels(index_plot, rotation ='vertical',fontsize=7)
# ax.set_title('Number of NAN per feature')
# # plt.legend()

# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')

# autolabel(bars)

# fig.tight_layout()

# fig.savefig('null_features_bars.png')

features_inf = np.isinf(features).sum().sort_values(ascending = False) # check number of inf values per column | max registered was 1304
# PLOT INF **************
# values = []
# index_plot = []
# counter = 1
# for feat in features_inf.index:
#     values.append(features_inf[feat])
#     index_plot.append(feat)
#     if features_inf[feat] == 0:
#         break
#     counter += 1
# x = np.arange(len(index_plot))  # the label locations
# width = 0.4  # the width of the bars
# fig, ax = plt.subplots()

# bars = ax.bar(x, values, width)

# ax.set_ylabel('Number of inf')
# ax.set_xlabel('Features')
# ax.set_xticks(x)
# ax.set_xticklabels(index_plot, rotation ='vertical',fontsize=7)
# ax.set_title('Number of inf per feature')
# # plt.legend()

# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     counter = 1
#     for rect in rects:
#         if (counter % 2) == 1:
#             height = rect.get_height()
#             ax.annotate('{}'.format(height),
#                         xy=(rect.get_x() + rect.get_width() / 2, height),
#                         xytext=(0, 1),  # 1 points vertical offset
#                         textcoords="offset points",
#                         ha='center', va='bottom')
#         counter += 1
# autolabel(bars)

# fig.tight_layout()

# fig.savefig('inf_features_bars.png')



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

# PLOT HEATMAP***********************************************************************
# fig, ax = plt.subplots(figsize=(24, 18))
# ax = sns.heatmap(df_correlation, annot = True, vmin=-1, vmax = 1, fmt='.2')
# ax.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
# add the column names as labels
# ax.set_yticklabels(df.columns, rotation = 0)
# ax.set_xticklabels(df.columns)
# plt.savefig('figure_huge.png', dpi=300)