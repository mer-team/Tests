import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_val_score, RepeatedStratifiedKFold, cross_validate

# to ignore the multiple "UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior." using cross_validate. Caused by zero predictions of one of the classes during the firt runs (1 feature)
import warnings
warnings.filterwarnings('once')

# read csv file with features
csvFile = pd.read_csv('./datasets/lyrics_features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
features = csvFile.drop(['quadrant', 'music.name'], axis=1)
headers = list(csvFile.drop(['quadrant','music.name'], axis=1))

print("total features: ", len(headers))
print("total songs: ", len(targets))

# normalization between 0 and 1
scaled_features = preprocessing.MinMaxScaler().fit_transform(features)

# select best features with chi2
bestFeatures = SelectKBest(score_func=chi2, k='all')
fit = bestFeatures.fit(scaled_features, targets)
dfScores = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(headers)
featureScores = pd.concat([dfColumns,dfScores], axis=1)
featureScores.columns = ['Features', 'Scores']

# writing features score
fs_list = pd.DataFrame(featureScores)
fs_list.to_csv('./chi2_features_weight.csv', index = False, mode='w')

# order + select features by ranking
features_sorted = featureScores.sort_values(by='Scores', ascending = False)
# writing ordered features score
features_sorted.to_csv('./chi2_features_weight_sorted.csv', index = False, mode='w')
