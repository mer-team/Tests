import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv file with features
csvFile = pd.read_csv('./accuracy_audio.csv', sep = ";", index_col=False)

# order csv by meanScore and get only first row (max meanScore)
sorted_csvFile = csvFile.sort_values(by = 'meanScore', ascending = False).copy()
maxRow = sorted_csvFile.head(1)
print('Max accuracy is ', maxRow['meanScore'].to_string(index=False), ' with ', maxRow['numFeatures'].to_string(index=False), ' features')

# PLOT
fig = plt.figure(figsize=(10,5))
plt.plot(csvFile['numFeatures'], csvFile['meanScore'], 
label='Max accuracy is ' + maxRow['meanScore'].to_string(index=False) + ' with ' + maxRow['numFeatures'].to_string(index=False) + ' features')
# xLabes between 100 and final - list(np.arange(100, max(csvFile['numFeatures']), 30)) - np.arange(start, stop, step)
xLabes = [0, 20, 40, 60, 80, 100, 130, 160, 190, 220, 250, 280, 310, 340, 370, 400, 430, 460, 490, 520, 550, 580, 610, 640, 670, 700, 730, 760, 790, 820, 850, 880, 910, 940, 970]
plt.xticks(xLabes, rotation = 65, fontsize=8)
plt.xlabel('Number of Features')
plt.ylabel('Accuracy')
# legend location plt.legend(bbox_to_anchor=(x, y))
plt.legend(loc = 'lower center')

# horizontal line - plt.hlines(y, xMin, xMax) | vertical line - plt.vlines(x, yMin, yMax)
plt.hlines(maxRow['meanScore'], 0, maxRow['numFeatures'], linestyle='dashed', colors = 'r')
plt.vlines(maxRow['numFeatures'], min(csvFile['meanScore']), maxRow['meanScore'], linestyle="dashed", colors = 'r')
plt.savefig('Accuracy_audio.png')