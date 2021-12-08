import pandas as pd
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, RepeatedStratifiedKFold

# to ignore the multiple "UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior." using cross_validate. Caused by zero predictions of one of the classes during the firt runs (1 feature)
import warnings
import json
warnings.filterwarnings('once')

# import dataset
csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant'].values
features = csvFile.drop(['quadrant', 'music.name'], axis=1).values
headers = list(csvFile.drop(['quadrant','music.name'], axis=1))

print("total features: ", len(headers))
print("total songs: ", len(targets))
#print(headers)

# load feature ranking
feat_ranking = pd.read_csv('./TuRF_allfeatures_ordered.csv', sep = ",", index_col=False)

# number of features to use
total_features = 220
score_array = ['f1_micro', 'f1_macro', 'accuracy', 'precision_micro', 'precision_macro', 'recall_micro', 'recall_macro']

# do we have feature indexes or names? iloc or loc?
feat_names = feat_ranking.loc[0:(total_features-1),"feature"]
features_ranked = csvFile.loc[:, feat_names]

# scale all features (ranked by importance)
scaled_features = preprocessing.MinMaxScaler().fit_transform(features_ranked)

# set up classifier and parameters optimization to use
param_grid = [
                    {
                        'kernel': ['linear'],
                        'C': [0.1, 1, 10, 100, 1000]
                    },
                    {
                        'kernel': ['rbf'],
                        'C': [0.1, 1, 10, 100, 1000],
                        'gamma': [1, 0.1, 0.01, 0.001, 0.0001]
                    }]

cv = RepeatedStratifiedKFold(
    n_splits=10, n_repeats=10, random_state=0
)

clf = GridSearchCV(svm.SVC(), param_grid, cv=cv, verbose=5, n_jobs=46)
#clf.fit(scaled_features, targets)
# print best parameter after tuning
# print(grid.best_params_)
# print how our model looks after hyper-parameter tuning
# print(grid.best_estimator_)

scores = cross_validate(clf, scaled_features, targets, cv=cv, n_jobs=46, verbose=1, return_train_score = True, scoring=score_array)

print...

json = json.dumps(scores)
f = open("run_best_features.json","w")
f.write(json)
f.close()


>>> from sklearn.metrics import confusion_matrix
>>> y_true = [2, 0, 2, 2, 0, 1]
>>> y_pred = [0, 0, 2, 2, 0, 2]
>>> confusion_matrix(y_true, y_pred)
array([[2, 0, 0],
       [0, 0, 1],
       [1, 0, 2]])
https://medium.com/analytics-vidhya/generation-of-a-concatenated-confusion-matrix-in-cross-validation-912485c4a972