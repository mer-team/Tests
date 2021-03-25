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
features_accompaniment = csvFile.iloc[:,0:4034].copy()
features_original = csvFile.iloc[:,4034:(8068)].copy()
features_vocals = csvFile.iloc[:,8068:].copy()

# NAN AND INF **************************************
# features_null = features_accompaniment.isnull().sum().sort_values(ascending = False) # check number of NAN values per column | max registered was 18
# # features_null.to_csv('./features_null.csv', mode='w')

# features_inf = np.isinf(features).sum().sort_values(ascending = False) # check number of inf values per column | max registered was 1304

# # STANDARD DEVIATION  ***********************************************************************
# std = features.std().sort_values()
# counter = 0
# to_drop = []
# for feature in std.index:
#     if std[feature] == 0:
#         to_drop.append(feature)
# df = features.drop(to_drop, axis=1)
# # print(df)

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
# ax.set_title('Number of NAN per features_accompaniment')
# # plt.legend()
# for i, v in enumerate(values):
#     ax.text(v, i , " {:.2f}".format(float(v)) + " %",va='center', color="blue", fontweight='bold')

# plt.savefig('null_features.png', format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures

# import os
# import numpy as np
# import matplotlib.pyplot as plt

# x = [u'INFO', u'CUISINE', u'TYPE_OF_PLACE', u'DRINK', u'PLACE', u'MEAL_TIME', u'DISH', u'NEIGHBOURHOOD']
# y = [160, 167, 137, 18, 120, 36, 155, 130]

# fig, ax = plt.subplots()    
# width = 0.75 # the width of the bars 
# ind = np.arange(len(y))  # the x locations for the groups
# ax.barh(ind, y, width, color="blue")
# ax.set_yticks(ind+width/2)
# ax.set_yticklabels(x, minor=False)
# plt.title('title')
# plt.xlabel('x')
# plt.ylabel('y')      

# for i, v in enumerate(y):
#     ax.text(v + 3, i , str(v) + " %",va='center', color='blue', fontweight='bold')
# #plt.show()
# plt.savefig(os.path.join('test.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures


# ****************************PLOT INF****************************
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