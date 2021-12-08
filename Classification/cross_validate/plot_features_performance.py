import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv files with features for ranking alg. Chi2 and TuRF
# Chi2
chi2_features = pd.read_csv('./cross_validate/bestK_search_results_set_vocal_rank_chi2_kernel_poly.csv', sep = ",", index_col=False)
# TuRF
turf_features = pd.read_csv('./cross_validate/bestK_search_results_set_vocals_rank_TuRF_kernel_poly.csv', sep = ",", index_col=False)

# order csv by f1_macro_mean and get only first row (max accuracy)
sorted_csvFile = chi2_features.sort_values(by = ['f1_macro_mean', 'numFeatures'], ascending = (False, True)).copy()
max_row_chi2 = sorted_csvFile.head(1)
sorted_csvFile = turf_features.sort_values(by = ['f1_macro_mean', 'numFeatures'], ascending = (False, True)).copy()
max_row_turf = sorted_csvFile.head(1)

# print(max_row_chi2['f1_macro_mean'])
# print(max_row_turf['f1_macro_mean'])

# PLOT
fig = plt.figure(figsize=(10,5))
plt.title('Performance for vocals dataset')

# plot chi2
plt.plot(chi2_features['numFeatures'], chi2_features['f1_macro_mean'], 
label='Max =' + max_row_chi2['f1_macro_mean'].to_string(index=False) + ' with' + max_row_chi2['numFeatures'].to_string(index=False) + ' features | Chi2')

# plot TuRF
plt.plot(turf_features['numFeatures'], turf_features['f1_macro_mean'], 
label='Max =' + max_row_turf['f1_macro_mean'].to_string(index=False) + ' with' + max_row_turf['numFeatures'].to_string(index=False) + ' features | TuRF')

# plot max value
plt.plot(max_row_chi2['numFeatures'], max_row_chi2['f1_macro_mean'], 'r+', ms=8, mew= 2)

# legend location
plt.legend(loc = 'lower center')

# concatenate two lists - the step is X before 100 and Y until the end
xLabes = np.concatenate((list(np.arange(0, 100, 10)), list(np.arange(100,max(chi2_features['numFeatures']), 15))))

plt.xticks(xLabes, rotation = 55, fontsize=9)
plt.xlabel('Number of Features')
plt.ylabel('Macro F1-score')
plt.ylim(0.45, 0.623)

plt.savefig('vocal.png')