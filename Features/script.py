import pprint
import essentia
import essentia.standard as es
import json

lst = ["min", "max", "median", "mean", "var", "skew", "kurt", "dmean", "dvar", "dmean2", "dvar2"]

features, features_frames = es.MusicExtractor(lowlevelStats=lst,
                                              rhythmStats=lst,
                                              tonalStats=lst,
                                              mfccStats=lst,
                                              gfccStats=lst)("song.wav")

# es.YamlOutput(filename = 'features.json', format = 'json')(features)

for key in features.descriptorNames():
    print(str(key) + ": " + str(features[key]))

# help(essentia.standard.MusicExtractor)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(sorted(features.descriptorNames())) # See all feature names in the pool in a sorted order
# print('Number of features:', len(features.descriptorNames())) 
# print('Zero-Crossing Rate: ' + str(features['lowlevel.zerocrossingrate.mean'])) # Another feature extracted