import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing


csvFile = pd.read_csv('./lyrics_features_without_variance.csv', sep = ";", index_col=False)
targets = csvFile['Quadrant']
csvFile = csvFile.drop(['Music', 'Quadrant', 'Id'], axis=1)

# FEATURES BEFORE = 167 | AFTER = 122

#   ******************** FEATURES RANKING ***************************************************
min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

bestFeatures = SelectKBest(score_func=chi2, k='all')
fit = bestFeatures.fit(min_max_scaler, targets)
dfScores = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(csvFile.columns)
featureScores = pd.concat([dfColumns,dfScores], axis=1)
featureScores.columns = ['Features', 'Scores']

# ORDER FEATURES BY SCORE ASCENDING
sortedFeatures = pd.DataFrame()

featureScores = featureScores.sort_values(by="Scores", ascending=True)

# create dataframe with features from worst to better
for column in featureScores['Features']:
    sortedFeatures = pd.concat([sortedFeatures, csvFile[column]], axis=1)


#   ******************** CORRELATION MATRIX ***************************************************
df_correlation = sortedFeatures.corr().abs()

# https://www.dezyre.com/recipes/drop-out-highly-correlated-features-in-python
# the matrix is symmetric so only half of the matrix need to be used. The top half is being placed with NaN values
matrix = df_correlation.where(np.tril(np.ones(df_correlation.shape),k=-1).astype(bool))

to_drop = []
# Find index of featurecolumns with correlation greater than X
to_drop = [column for column in matrix.columns if any(matrix[column] > 0.7)]

csvFile = csvFile.drop(to_drop, axis=1)
print(csvFile) # features 122

csvFile.to_csv('./features_after_correlation.csv', mode='w', sep=';', index = False)