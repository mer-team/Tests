import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_val_score
import matplotlib.pyplot as plt

csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)

# normalization between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

# classifier
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                    'C': [1, 10, 100, 1000]},
                {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=5)

featuresNum = []
scoresMean = []
counter = 1
scoresdf = pd.DataFrame(columns=['numFeatures','meanScore','stdScore'])
scoresdf.to_csv('./scoresdf.csv', index = False, mode='w')

while counter < 100:
    bestFeatures = SelectKBest(score_func=chi2, k=counter)
    fit = bestFeatures.fit(min_max_scaler, targets)
    dfScores = pd.DataFrame(fit.scores_)
    dfColumns = pd.DataFrame(csvFile.columns)
    featureScores = pd.concat([dfColumns,dfScores], axis=1)
    featureScores.columns = ['Features', 'Scores']

    kbest = fit.get_support() 
    dfAux = csvFile.iloc[:, kbest].copy() # get only best features from dataframe

    scaler = preprocessing.StandardScaler().fit(dfAux)
    scaled_values = scaler.transform(dfAux) 

    scores = cross_val_score(clf, scaled_values, targets, cv=5, n_jobs=-1)
    scoresRow = pd.DataFrame({'numFeatures':[counter], 
    'meanScore':["{:.3f}".format(scores.mean())],
    'stdScore':["{:.3f}".format(scores.std())]})
    scoresRow.to_csv('./scoresdf.csv', header=False, index = False, mode='a')
    print(counter)
    counter +=1

while counter > 99 and counter <= len(csvFile.columns):
    bestFeatures = SelectKBest(score_func=chi2, k=counter)
    fit = bestFeatures.fit(min_max_scaler, targets)
    dfScores = pd.DataFrame(fit.scores_)
    dfColumns = pd.DataFrame(csvFile.columns)
    featureScores = pd.concat([dfColumns,dfScores], axis=1)
    featureScores.columns = ['Features', 'Scores']

    kbest = fit.get_support() 
    dfAux = csvFile.iloc[:, kbest].copy() # get only best features from dataframe

    scaler = preprocessing.StandardScaler().fit(dfAux)
    scaled_values = scaler.transform(dfAux) 

    scores = cross_val_score(clf, scaled_values, targets, cv=5, n_jobs=-1)
    scoresRow = pd.DataFrame({'numFeatures':[counter], 
    'meanScore':["{:.3f}".format(scores.mean())],
    'stdScore':["{:.3f}".format(scores.std())]})
    scoresRow.to_csv('./scoresdf.csv', header=False, index = False, mode='a')
    print(counter)
    counter +=5