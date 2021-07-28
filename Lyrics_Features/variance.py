import pandas as pd

csvFile = pd.read_csv('./lyrics_features_without_null.csv', sep = ";", index_col=False)
csvFile = csvFile.drop(['Music', 'Quadrant', 'Id'], axis=1)

#   ******************** VARIANCE ***************************************************
# REMOVE OUTLIERS
# https://www.pluralsight.com/guides/cleaning-up-data-from-outliers
# The interquartile range (IQR) is a measure of statistical dispersion 
# and is calculated as the difference between the 75th and 25th percentiles.
# It is represented by the formula IQR = Q3 − Q1

Q1 = csvFile.quantile(0.25)
Q3 = csvFile.quantile(0.75)
IQR = Q3 - Q1
data_clean = csvFile[~((csvFile < (Q1-1.5*IQR)) | (csvFile > (Q3+1.5*IQR)))]

# VARIANCE - before - 198 |  after - 167 features
var = data_clean.var().sort_values()
print(var)
to_drop = []
for feature in var.index:
    if var[feature] < 0.0000001:
        to_drop.append(feature)
csvFile = csvFile.drop(to_drop, axis=1)

csvFile.to_csv('./lyrics_features_without_variance.csv', mode='w', sep=';', index = False)