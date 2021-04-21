import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold


csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)


#   ******************** FEATURES RANKING ***************************************************
min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

bestFeatures = SelectKBest(score_func=chi2, k=10)
fit = bestFeatures.fit(min_max_scaler, targets)
dfScores = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(csvFile.columns)
featureScores = pd.concat([dfColumns,dfScores], axis=1)
featureScores.columns = ['Features', 'Scores']

featureScores = featureScores.sort_values(by="Scores", ascending=False)

kbest = fit.get_support() 
csvFile = csvFile.iloc[:, kbest] # get only best features from dataframe