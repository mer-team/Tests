import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_val_score, RepeatedStratifiedKFold, cross_validate

# to ignore the multiple "UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior." using cross_validate. Caused by zero predictions of one of the classes during the firt runs (1 feature)
import warnings
warnings.filterwarnings('once')

# read csv file with features
csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
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
# fs_list = pd.DataFrame(featureScores)
# fs_list.to_csv('./chi2_features_weight.csv', index = False, mode='w')

# order + select features by ranking
features_sorted = featureScores.sort_values(by='Scores', ascending = False)
# writing ordered features score
features_sorted.to_csv('./chi2_features_weight_sorted.csv', index = False, mode='w')

head = ""
to_use = pd.DataFrame()
for feature in features_sorted.Features:
    # head = head + feature + ", "
    to_use = pd.concat([to_use, features[feature]], axis=1)

# to_use.to_csv('./chi2_features_weight_use.csv', index = False, mode='w', sep=';')


# scale all features (ranked by importance)
scaled_features = preprocessing.MinMaxScaler().fit_transform(to_use)

# set up classifier and parameters optimization to use
tuned_parameters = [{'kernel': ['linear'], 'C': [1, 10]}]

cv = RepeatedStratifiedKFold(
    n_splits=10, n_repeats=10, random_state=0
)

clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=cv)

counter = 1
# column names for csv file - scoresdf_chi2.csv
columns_to_write = ['numFeatures', 'fit_time_mean', 'fit_time_std','score_time_mean', 'score_time_std', 'f1_micro_mean', 'f1_micro_std', 'f1_macro_mean', 'f1_macro_std', 'accuracy_mean', 'accuracy_std', 'precision_micro_mean', 'precision_micro_std', 'precision_macro_mean', 'precision_macro_std', 'recall_micro_mean', 'recall_micro_std', 'recall_macro_mean', 'recall_macro_std']

scoresdf_chi2 = pd.DataFrame(columns=columns_to_write)
scoresdf_chi2.to_csv('./scoresdf_chi2.csv', index = False, columns=columns_to_write, mode='w')

while counter <= len(headers):
    # cross validation using all cores (n_jobs=-1) and cross validation = 10
    # scores = cross_val_score(clf, scaled_features[:,range(0,counter)], targets, cv=cv, n_jobs=46, scoring=['f1_micro', 'f1_macro', 'accuracy', 'precision', 'recall'])
    scores = cross_validate(clf, scaled_features[:,range(0,counter)], targets, cv=cv, n_jobs=-1, scoring=['f1_micro', 'f1_macro', 'accuracy', 'precision_micro', 'precision_macro', 'recall_micro', 'recall_macro'])

    # build row to insert into csv file
    scoresRow = pd.DataFrame({
        'numFeatures':[counter],
        'fit_time_mean':["{:.3f}".format(scores['fit_time'].mean())],
        'fit_time_std':["{:.3f}".format(scores['fit_time'].std())],
        'score_time_mean':["{:.3f}".format(scores['score_time'].mean())],
        'score_time_std':["{:.3f}".format(scores['score_time'].std())],
        'f1_micro_mean':["{:.3f}".format(scores['test_f1_micro'].mean())],
        'f1_micro_std':["{:.3f}".format(scores['test_f1_micro'].std())],
        'f1_macro_mean':["{:.3f}".format(scores['test_f1_macro'].mean())],
        'f1_macro_std':["{:.3f}".format(scores['test_f1_macro'].std())],
        'accuracy_mean':["{:.3f}".format(scores['test_accuracy'].mean())],
        'accuracy_std':["{:.3f}".format(scores['test_accuracy'].std())],
        'precision_micro_mean':["{:.3f}".format(scores['test_precision_micro'].mean())],
        'precision_micro_std':["{:.3f}".format(scores['test_precision_micro'].std())],
        'precision_macro_mean':["{:.3f}".format(scores['test_precision_macro'].mean())],
        'precision_macro_std':["{:.3f}".format(scores['test_precision_macro'].std())],
        'recall_micro_mean':["{:.3f}".format(scores['test_recall_micro'].mean())],
        'recall_micro_std':["{:.3f}".format(scores['test_recall_micro'].std())],
        'recall_macro_mean':["{:.3f}".format(scores['test_recall_macro'].mean())],
        'recall_macro_std':["{:.3f}".format(scores['test_recall_macro'].std())]
    })
    scoresRow.to_csv('./scoresdf_chi2.csv', header=False, index = False, columns=columns_to_write, mode='a')
    print("feats: ", counter, ", accuracy: ", "{:.3f}".format(scores['test_accuracy'].mean()))
    if (counter < 100):
        counter +=1
    else:
        counter +=10
