import subprocess
import csv
import pandas as pd
import os

dataset_path = '/vagrant/Lyrics_dataset/'

# FEATURES
counter = 1
for folder in sorted(os.listdir(dataset_path)):
    for audio in sorted(os.listdir(dataset_path + folder)):
        path = dataset_path + folder + '/' + audio
        # USE  subprocess.run TO GET OUTPUT
        result = subprocess.check_output(['java', '-jar', 'MainInterface.jar', 'all_features', path, 'intermediate_output.csv']) 
        df2 = pd.DataFrame()
        # read csv
        df2 = pd.read_csv('./intermediate_output.csv', sep = ",", index_col=False)
        if counter == 1:
            df2.to_csv('./features_lyrics.csv', index = False, mode='a')
        else:
            df2.to_csv('./features_lyrics.csv', index = False, mode='a', header = 0)
        print(counter)
        counter += 1

# QUADRANTS
features = pd.read_csv('./features_lyrics.csv', sep = ",", index_col=False)
quadrants = pd.read_csv('./Quadrantes-771180.csv', sep = ",", index_col=False)
# quadrants = quadrants.drop(['Music'], axis=1)
frames = [quadrants, features]
result =  pd.concat(frames, axis=1)
result.to_csv('./lyrics_features_extracted.csv', index = False, mode='w')
