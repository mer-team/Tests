import pprint
import essentia
import essentia.standard as es

pp = pprint.PrettyPrinter(indent=4)

# help(essentia.standard.MusicExtractor)

features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])('./song.wav')

# pp.pprint(sorted(features.descriptorNames())) # See all feature names in the pool in a sorted order
# print('Number of features:', len(features.descriptorNames())) # 161
# print(features['lowlevel.zerocrossingrate.mean']) # Another feature extracted

print("Filename:", features['metadata.tags.file_name'])
print("-" * 80)
print("Pitch Salience:")
print("                Mean:", features['lowlevel.pitch_salience.mean'])
print("                StDev:", features['lowlevel.pitch_salience.stdev'])
print("-" * 80)
print("Loudness:",features['lowlevel.average_loudness'])
print("-" * 80)
print("BPM:", features['rhythm.bpm'])
print("Beat positions (sec.)", features['rhythm.beats_position'])