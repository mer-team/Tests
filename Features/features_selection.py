import csv
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import preprocessing
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./features_new.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)
features = csvFile.replace([np.inf, -np.inf], np.nan)
# features_accompaniment = features.iloc[:,0:4034].copy()
# features_original = features.iloc[:,4034:(8068)].copy()
features_vocals = features.iloc[:,8068:].copy()

# GENERATE MIN VALUES FOR FEATURES_VOCALS WHERE MUSIC IS SILENT
# min = features_vocals.min()
# min = pd.DataFrame(min).T # TO ROW
# min.to_csv('./min_vocals.csv', mode='w', index = False, header = False)

# NAN AND INF **************************************
features_null = features_vocals.isnull().sum().sort_values(ascending = False) # check number of NAN values per column | max registered was 18
print(features_null)

# # STANDARD DEVIATION  ***********************************************************************
# std = csvFile.std().sort_values()
# to_drop = []
# for feature in std.index:
#     if std[feature] == 0:
#         to_drop.append(feature)
# df = features.drop(to_drop, axis=1)
# print(df)

# df_correlation = df.corr().abs()

# # https://www.dezyre.com/recipes/drop-out-highly-correlated-features-in-python
# upper_tri = df_correlation.where(np.triu(np.ones(df_correlation.shape),k=1).astype(np.bool))

# # IF CORRELATION = 1 ***********************************************************************
# # correlation_equals_1 = [column for column in upper_tri.columns if any(upper_tri[column] == 1)]
# # print(correlation_equals_1) 
# # print('Number of features: ' + str(len(correlation_equals_1)))

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

# ****************************PLOT NAN****************************
# values = []
# index_plot = []
# counter = 1
# for feat in features_null.index:
#     value = (features_null[feat] * 100) / 900 # 900 musics - 100% | features_null[feat] musics- x %
#     values.append(value)
#     index_plot.append(feat)
#     if features_null[feat] == 0:
#         break
#     counter += 1
# x = np.arange(len(index_plot))  # the label locations
# width = 0.5  # the width of the bars
# fig, ax = plt.subplots()
# bars = ax.barh(x, values, width, linewidth = 0, color=(0.2, 0.4, 0.6, 0.6))
# ax.invert_yaxis() # invert y axis to show lowest value below
# plt.xlim(0,np.max(values)*1.2) # change outside rect width - limit x
# ax.set_yticks(x)
# ax.set_yticklabels(index_plot, minor=False)
# # ax.invert_yaxis()  # labels read top-to-bottom
# ax.xaxis.set_visible(False)
# ax.set_title('Number of NAN on features_vocals')
# # plt.legend()
# for i, v in enumerate(values):
#     ax.text(v, i , " {:.2f}".format(float(v)) + " %",va='center', color="blue", fontweight='bold')

# plt.savefig('null_features.png', format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures