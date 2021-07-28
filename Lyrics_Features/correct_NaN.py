import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./lyrics_features_extracted.csv', sep = ";", index_col=False)
features = csvFile.drop(['Music', 'Quadrant', 'Id'], axis=1)

# ********************** List number of NAN **************************************
# features_null = features.isnull().sum().sort_values(ascending = False)
# print(features_null)
# ********************** Fill NaNs with median values **************************************

median = features.median()
print(median)
for feature in median.index:
    features[feature] = features[feature].replace(np.nan, median[feature])

features.to_csv('./lyrics_features_without_null.csv', sep=';', mode='w', index = False)
# # ****************************PLOT NAN****************************
# features_null = features.isnull().sum().sort_values(ascending = False)
# values = []
# index_plot = []
# counter = 1
# # features_null is a serie with all column names and number of null values
# for feat in features_null.index:
#     # get value in %
#     value = (features_null[feat] * 100) / 951 # 951 musics - 100% | features_null[feat] musics- x %
#     values.append(value)
#     index_plot.append(feat)
#     if features_null[feat] == 0:
#         break
#     counter += 1
# x = np.arange(len(index_plot))  # the label locations
# width = 0.4  # the width of the bars
# fig, ax = plt.subplots()
# bars = ax.barh(x, values, width, linewidth = 0, color=(0.2, 0.4, 0.6, 0.6))
# ax.invert_yaxis() # invert y axis to show lowest value below
# plt.xlim(0,np.max(values)*1.3) # change outside rect width - limit x
# ax.set_yticks(x)
# ax.set_yticklabels(index_plot, minor=False)

# ax.xaxis.set_visible(False)
# ax.set_title(str(features_null.sum()) + ' Null (NaN) features for lyrics dataset') # number of features + string
# plt.plot([], [], ' ', label="% - Number of features") # create empty plot just with label
# plt.legend(loc='lower right')
# for i, v in enumerate(values):
#     ax.text(v, i , " {:.2f}".format(float(v)) + " % - " + str(int((v * 951) / 100)), va='center', color="blue")

# plt.savefig('Null_Features_Lyrics.png', format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures