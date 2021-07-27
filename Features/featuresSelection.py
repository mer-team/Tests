import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_val_score, RepeatedStratifiedKFold

# read csv file with features
csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)

# normalization between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

#TO DO: use linear kernel because it has the best performance
# classifier
tuned_parameters = [{'kernel': ['linear'], 'C': [1, 10]}]

cv = RepeatedStratifiedKFold(
    n_splits=10, n_repeats=10, random_state=0
)

clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=cv)

counter = 1
# column names for csv file - scoresdf.csv
# this csv file must have three columns - number of features and its mean and std score
scoresdf = pd.DataFrame(columns=['numFeatures','meanScore','stdScore'])
scoresdf.to_csv('./scoresdf.csv', index = False, mode='w')


# two equal cycles. Up to iteration 100, the feature number is iterated with the value 1
# then it is incremented from 5 to 5
while counter < 3:
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
    # cross validation using all cores (n_jobs=-1) and cross validation = 10
    scores = cross_val_score(clf, scaled_values, targets, cv=cv, n_jobs=-1)
    # build row to insert into csv file
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

    # cross validation using all cores (n_jobs=-1) and cross validation = 10
    scores = cross_val_score(clf, scaled_values, targets, cv=10, n_jobs=-1)

    # build row to insert into csv file
    scoresRow = pd.DataFrame({'numFeatures':[counter], 
    'meanScore':["{:.3f}".format(scores.mean())],
    'stdScore':["{:.3f}".format(scores.std())]})
    scoresRow.to_csv('./scoresdf.csv', header=False, index = False, mode='a')
    print(counter)
    counter +=5