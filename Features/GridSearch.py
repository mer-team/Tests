import pandas as pd
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold
from sklearn.svm import SVC
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, chi2

csvFile = pd.read_csv('./features_after_correlation.csv', sep = ";", index_col=False)
targets = csvFile['quadrant']
csvFile = csvFile.drop(['quadrant', 'music.name'], axis=1)

min_max_scaler = preprocessing.MinMaxScaler().fit_transform(csvFile)

bestFeatures = SelectKBest(score_func=chi2, k=(25))
fit = bestFeatures.fit(min_max_scaler, targets)
dfScores = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(csvFile.columns)
featureScores = pd.concat([dfColumns,dfScores], axis=1)
featureScores.columns = ['Features', 'Scores']

kbest = fit.get_support() 
dfAux = csvFile.iloc[:, kbest].copy() # get only best features from dataframe


param_grid = [
    {'kernel': ['linear']},
    {'kernel': ['poly'], 'degree': [2, 3]},
    {'kernel': ['rbf']}
]

svc = SVC(random_state=0)

cv = RepeatedStratifiedKFold(
    n_splits=10, n_repeats=10, random_state=0
)

search = GridSearchCV(
    estimator=svc, param_grid=param_grid,
     cv=cv, n_jobs = -1
)
search.fit(dfAux, targets)

results_df = pd.DataFrame(search.cv_results_)
results_df = results_df.sort_values(by=['rank_test_score'])
results_df = (
    results_df
    .set_index(results_df["params"].apply(
        lambda x: "_".join(str(val) for val in x.values()))
    )
    .rename_axis('kernel')
)
results_df[
    ['params', 'rank_test_score', 'mean_test_score', 'std_test_score']
]
print("results df")
print(results_df)

# create df of model scores ordered by perfomance
model_scores = results_df.filter(regex=r'split\d*_test_score')

# plot 30 examples of dependency between cv fold and AUC scores
fig, ax = plt.subplots()
sns.lineplot(
    data=model_scores.transpose().iloc[:30],
    dashes=False, palette='Set1', marker='o', alpha=.5, ax=ax
)
ax.set_xlabel("CV test fold", size=12, labelpad=10)
ax.set_ylabel("Model AUC", size=12)
ax.tick_params(bottom=True, labelbottom=False)
plt.savefig('figure.png')

# print correlation of AUC scores across folds
print(f"Correlation of models:\n {model_scores.transpose().corr()}")