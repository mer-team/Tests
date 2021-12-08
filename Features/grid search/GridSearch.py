import pandas as pd
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from sklearn.svm import SVC
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

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
features_grid = [10, 25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
#score_array = ['f1_micro', 'f1_macro', 'accuracy', 'precision_micro', 'precision_macro', 'recall_micro', 'recall_macro']

for total_features in features_grid:
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
                        'kernel': ['poly'],
                        'degree': [2, 3, 4],
                        'C': [0.1, 1, 10, 100, 1000],
                        'gamma': [1, 0.1, 0.01, 0.001, 0.0001, 'scale', 'auto']
                    },
                    {
                        'kernel': ['rbf'],
                        'C': [0.1, 1, 10, 100, 1000],
                        'gamma': [1, 0.1, 0.01, 0.001, 0.0001, 'scale', 'auto']
                    },
                    {
                        'kernel': ['sigmoid'],
                        'C': [0.1, 1, 10, 100, 1000],
                        'gamma': [1, 0.1, 0.01, 0.001, 0.0001, 'scale', 'auto']
                    }]
    # set up classifier and parameters optimization to use
    # param_grid = [
    #                     {
    #                         'kernel': ['linear'],
    #                         'C': [0.1, 1]
    #                     },
    #                     {
    #                         'kernel': ['rbf'],
    #                         'C': [0.1, 1, 10],
    #                         'gamma': [1, 0.1]
    #                     }]
    svc = SVC(random_state=0)
    cv = RepeatedStratifiedKFold(
        n_splits=10, n_repeats=10, random_state=0
    )
    search = GridSearchCV(
        estimator=svc, param_grid=param_grid,
        scoring='f1_macro',
        cv=cv, n_jobs = 46, verbose=5
    )
    search.fit(scaled_features, targets)
    results_df = pd.DataFrame(search.cv_results_)
    results_df = results_df.sort_values(by=['rank_test_score'])
    results_df = (
        results_df
        .set_index(results_df["params"].apply(
            lambda x: "_".join(str(val) for val in x.values()))
        )
        .rename_axis('kernel')
    )
    results_summary = results_df[
        ['params', 'rank_test_score', 'mean_test_score', 'std_test_score']
    ]
    results_filename = "grid_search_results_{}_features_{}_params.csv".format(total_features, len(results_summary))
    results_summary.to_csv(results_filename, index = True, mode='w')
    print(results_summary)


# print(results_df)

# # create df of model scores ordered by perfomance
# model_scores = results_df.filter(regex=r'split\d*_test_score')

# # plot 30 examples of dependency between cv fold and AUC scores
# fig, ax = plt.subplots()
# sns.lineplot(
#     data=model_scores.transpose().iloc[:30],
#     dashes=False, palette='Set1', marker='o', alpha=.5, ax=ax
# )
# ax.set_xlabel("CV test fold", size=12, labelpad=10)
# ax.set_ylabel("F1-score (macro)", size=12)
# ax.tick_params(bottom=True, labelbottom=False)
# plt.savefig('figure.png')

# # print correlation of AUC scores across folds
# print(f"Correlation of models:\n {model_scores.transpose().corr()}")

# # from https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_stats.html