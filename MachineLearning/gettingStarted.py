# from sklearn.ensemble import RandomForestClassifier

# clf = RandomForestClassifier(random_state=0)
# X = [[ 1,  2,  3], [11, 12, 13]] # 2 samples, 3 features
# y = [0, 1]  # classes of each sample

# clf.fit(X, y)

# clf.predict(X)  # predict classes of the training data

# print(clf.predict([[14, 15, 16],[4, 5, 6] ]))  # predict classes of new data

# **********************************************************************************

# from sklearn.preprocessing import StandardScaler
# X = [[0, 15],
#      [1, -10]]
# print(StandardScaler().fit(X).transform(X))

# **********************************************************************************

from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate

X, y = make_regression(n_samples=1000, random_state=0)
lr = LinearRegression()


# result = cross_validate(lr, X, y)  # defaults to 5-fold CV

result = cross_validate(lr, X, y, cv=10)  # 10-fold CV

print(result['test_score'])  # r_squared score is high because dataset is easy

# **********************************************************************************
