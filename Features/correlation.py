import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn import preprocessing

csvFile = pd.read_csv('./features_without_null.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)

# features_accompaniment = csvFile.iloc[:,0:4034].copy()
# features_original = csvFile.iloc[:,4034:(8068)].copy()
# features_vocals = csvFile.iloc[:,8068:].copy()

#   ******************** VARIANCE ***************************************************
# REMOVE OUTLIERS
# https://www.pluralsight.com/guides/cleaning-up-data-from-outliers
# The interquartile range (IQR) is a measure of statistical dispersion 
# and is calculated as the difference between the 75th and 25th percentiles.
# It is represented by the formula IQR = Q3 − Q1

Q1 = csvFile.quantile(0.25)
Q3 = csvFile.quantile(0.75)
IQR = Q3 - Q1
data_clean = csvFile[~((csvFile < (Q1-1.5*IQR)) | (csvFile > (Q3+1.5*IQR)))]

# VARIANCE - before - 1290 |  after - 9009 features
var = data_clean.var().sort_values()
to_drop = []
for feature in var.index:
    if var[feature] == 0:
        to_drop.append(feature)
csvFile = csvFile.drop(to_drop, axis=1)

#   ******************** FEATURES RANKING ***************************************************
# min_max_scaler = preprocessing.StandardScaler().fit_transform(csvFile) # mean value of 0 and a standard deviation of 1.
min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

bestFeatures = SelectKBest(score_func=chi2, k='all')
fit = bestFeatures.fit(min_max_scaler, targets)
dfScores = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(csvFile.columns)
featureScores = pd.concat([dfColumns,dfScores], axis=1)
featureScores.columns = ['Features', 'Scores']

sortedFeatures = pd.DataFrame()

featureScores = featureScores.sort_values(by="Scores", ascending=True)

for column in featureScores['Features']:
    sortedFeatures = pd.concat([sortedFeatures, csvFile[column]], axis=1)
# kbest = fit.get_support() 
# csvFile = csvFile.iloc[:, kbest] # get only best features from dataframe


#   ******************** CORRELATION MATRIX ***************************************************
df_correlation = sortedFeatures.corr().abs()

# https://www.dezyre.com/recipes/drop-out-highly-correlated-features-in-python
matrix = df_correlation.where(np.tril(np.ones(df_correlation.shape),k=-1).astype(np.bool))

to_drop = []
# Find index of featurecolumns with correlation greater than X
to_drop = [column for column in matrix.columns if any(matrix[column] > 0.7)]

csvFile = csvFile.drop(to_drop, axis=1)
print(csvFile) # features 1000

# csvFile.to_csv('./features_correlation.csv', mode='w')


# # ***********************************PLOTS*******************************
# # ****************************HEATMAP****************************
# fig, ax = plt.subplots()
# ax = sns.heatmap(matrix, annot = True, vmin=0, vmax = 1, fmt='.2', cmap='coolwarm')
# ax.set_title('Correlation Heatmap - Few features for example purposes', fontdict={'fontsize':12}, pad=12)
# # add the column names as labels
# labels = []

# for label in matrix.columns:
#     new_label = label.replace('lowlevel.', '')
#     new_label2 = new_label.replace('.accompaniment', '')
#     labels.append(new_label2)

# ax.set_yticklabels(labels, rotation = 0)
# ax.set_xticklabels(labels, rotation = 85)

# ax.xaxis.set_ticks_position("top")
# plt.savefig('features_heatmap.png', bbox_inches='tight')