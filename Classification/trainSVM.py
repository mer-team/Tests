import pandas as pd
from sklearn import svm
from sklearn import preprocessing
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

# variable 
path_dataset = './datasets/lyrics_features_after_correlation.csv'
path_ranking = './feature_ranking/chi2/lyrics/alljava_20210813/chi2_features_weight_sorted.csv'
num_of_features = 85
cost = 100
# degree = 4
gamma = 0.01
kernel = 'sigmoid'
classifier_name = './classifiers/lyrics_model.joblib'
scaler_name = './classifiers/lyrics_scaler.joblib'
# figure_title = 'Confusion Matrix for dataset of Audio - Vocal'
# figure_name = 'vocal_confusion_matrix.png'

# read dataset
dataset = pd.read_csv(path_dataset, sep = ";", index_col=False)
targets = dataset['quadrant']
features = dataset.drop(['quadrant', 'music.name'], axis=1)

# read only column Features and certain number of rows
# get n best features of ranking
ranking = pd.read_csv(path_ranking, sep = ",", index_col=False, usecols=['Features'], nrows=num_of_features)

to_use = pd.DataFrame()
for feature in ranking.Features:
    to_use = pd.concat([to_use, features[feature]], axis=1)

# standardization
scaler = preprocessing.MinMaxScaler().fit(to_use)
scaled_values = scaler.transform(to_use) 

# classifier
clf = svm.SVC(random_state = 0, kernel=kernel, C=cost, gamma=gamma)
clf.fit(scaled_values, targets) 

dump(clf, classifier_name)
dump(scaler, scaler_name)

# Q1 - Alegre | Happy
# Q2 - Tensa | tense
# Q3 - Triste | Sad
# Q4 - Calma | Calm

# # TEST CLASSIFIER

# X_train, X_test, y_train, y_test = train_test_split(to_use, targets, train_size=0.90, stratify=targets)

# scaler_test = preprocessing.StandardScaler().fit(X_train)
# scaled_values_train = scaler_test.transform(X_train) 
# scaled_values_test = scaler_test.transform(X_test) 

# clf.fit(scaled_values_train, y_train)
# y_pred = clf.predict(scaled_values_test)
# print(accuracy_score(y_test, y_pred))

# # PLOT
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,5))
# ax1, ax2 = axes.flatten()

# # normalize None = how often each combination of true and predicted category levels occurs
# # normalize true = relative frequencies per row. Each row is 1.00
# titles_options = [("Confusion matrix without normalization", None, ax1), ("Normalized confusion matrix", 'true', ax2)]
# fig.suptitle(figure_title, fontsize=14)
# for title, normalize, ax in titles_options:
#     disp = plot_confusion_matrix(clf, scaled_values_test, y_test, cmap=plt.cm.Blues, ax=ax, normalize=normalize)
#     disp.ax_.set_title(title)
#     disp.ax_.xaxis.set_ticklabels(['Alegre', 'Tensa', 'Triste', 'Calma'])
#     disp.ax_.yaxis.set_ticklabels(['Alegre', 'Tensa', 'Triste', 'Calma'])

# plt.savefig(figure_name)
