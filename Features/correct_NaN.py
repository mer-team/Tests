import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./features_new.csv', sep = ";", index_col=False)
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)
features = csvFile.replace([np.inf, -np.inf], np.nan)
# features_accompaniment = features.iloc[:,0:4034].copy()
# features_original = features.iloc[:,4034:(8068)].copy()
# features_vocals = features.iloc[:,8068:].copy()

# GENERATE MIN VALUES FOR FEATURES_VOCALS WHERE MUSIC IS SILENT
# min = features_vocals.min()
# min = pd.DataFrame(min).T # TO ROW
# min.to_csv('./min_vocals.csv', mode='w', index = False, header = False)


# ********************** Drop NAN **************************************
features_null = features.isnull().sum().sort_values(ascending = False)
to_drop = []
for feature in features_null.index:
    if features_null[feature] >= 450: # dataset has 900 songs - so 50% of the songs are 450
        to_drop.append(feature)
features = features.drop(to_drop, axis=1)

# ********************** Fill NaNs with median values **************************************

median = features.median()
for feature in median.index:
    features[feature] = features[feature].replace(np.nan, median[feature])

features.to_csv('./features_without_null.csv', sep=';', mode='w', index = False)

# ****************************PLOT NAN****************************
# features_null = features.isnull().sum().sort_values(ascending = False)
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
# ax.set_title('Null values (NaNs + Inf) of Features - Vocal')
# # plt.legend()
# for i, v in enumerate(values):
#     ax.text(v, i , " {:.2f}".format(float(v)) + " %",va='center', color="blue", fontweight='bold')

# plt.savefig('Null_Features_Vocal.png', format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures