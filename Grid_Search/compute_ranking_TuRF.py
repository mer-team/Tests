import pandas as pd
import numpy as np
from skrebate.turf import TuRF
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing, svm
from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, RepeatedStratifiedKFold

# to ignore the multiple "UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior." using cross_validate. Caused by zero predictions of one of the classes during the firt runs (1 feature)
import warnings
warnings.filterwarnings('once')

# import dataset
csvFile = pd.read_csv('./datasets/lyrics_features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant'].values
features = csvFile.drop(['quadrant', 'music.name'], axis=1).values
headers = list(csvFile.drop(['quadrant','music.name'], axis=1))

print("total features: ", len(headers))
print("total songs: ", len(targets))
#print(headers)

# select best features with TuRF + ReliefF
fs = TuRF(core_algorithm="ReliefF", n_features_to_select=len(headers), pct=0.4, n_jobs=-1, verbose=True)
# help(fs)
fs.fit(features, targets, headers)

# writing features weight
fs_list = pd.DataFrame(data = {'feature': headers, 'weight': fs.feature_importances_})
fs_list.to_csv('./TuRF_features_weight.csv', index = False, mode='w')

# top features to use:
print("TuRF indicated ", len(fs.top_features_), " top features")

# order + select features by ranking
features_ranked = features[:, fs.top_features_]
top_features_by_name = [headers[i] for i in fs.top_features_]

top_feats_list = pd.DataFrame(data = {
    'rank': range(1, len(fs.top_features_) + 1 ),
    'feature': top_features_by_name,
    'index': fs.top_features_})
top_feats_list.to_csv('./TuRF_top_features.csv', index = False, mode='w')

ordered_features_list = pd.DataFrame(data = {
    'index': range(0, len(headers)),
    'feature': headers,
    'weight': fs.feature_importances_})

df1 = ordered_features_list.sort_values(by=['weight'], ascending=False)
df1['rank'] = [*range(1, len(top_feats_list)+1)] + ['*'] * (len(headers) - len(top_feats_list))
#df1.at[0:len(top_feats_list),'rank'] = range(1, len(top_feats_list)+1)
df1.to_csv("./TuRF_allfeatures_ordered.csv", index = False, mode='w')
ordered_features_list.to_csv("./TuRF_allfeatures_original.csv", index = False, mode='w')

