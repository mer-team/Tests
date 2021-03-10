import essentia
import essentia.standard as es
import numpy
import csv
import os

# https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python?page=1&tab=votes#tab-top
def scaleNotation(x):
    return {
        'minor': 0,
        'major': 1
    }[x]

# https://en.wikipedia.org/wiki/Pitch_class
def keyNotation(x):
    return {
        'B#':0,
        'C':0,
        'C#':1,
        'Db':1,
        'D':2,
        'D#':3,
        'Eb':3,
        'E':4,
        'Fb':4,
        'F':5,
        'E#':5,
        'F#':6,
        'Gb':6,
        'G':7,
        'G#':8,
        'Ab':8,
        'A':9,
        'A#':10,
        'Bb':10,
        'B':11,
        'Cb':11
    }[x]

lst = ["min", "max", "median", "mean", "var", "skew", "kurt", "dmean", "dvar", "dmean2", "dvar2"]

##################################
# CSV HEADER
##################################

# Load pool from a JSON file
features = es.YamlInput(filename="./features_example.json", format="json")()                                       

out = open('features.csv', 'w')
for key in features.descriptorNames():
    if "metadata" in key:
        continue
    elif "rhythm.beats_position" in key:
        continue
    elif "rhythm.bpm_histogram" in key:
        continue
    elif isinstance(features[key], numpy.ndarray):
        counter = 1
        for value in features[key]:
            txt = key + "[" + str(counter) + "]"
            out.write('%s;' % txt)
            counter = counter + 1
    else:
        out.write('%s;' % key)

txt = "quadrant"
out.write('%s;' % txt)
out.write("\n")

##################################
# DATA
##################################


# quadrants
dataset = "/vagrant/datasetFinal/"
output = "/vagrant/datasetFeatures/"

musicNumber = 1

for source in os.listdir(dataset):
    # create folders for different sources
    dir = output + source + "/"
    try:
        os.mkdir(dir)
    except OSError:
        print ("Creation of the directory %s failed" % dir)
    else:
        print ("Successfully created the directory %s " % dir)

    for quadrant in os.listdir(dataset + source):
        # create folders for different quadrants
        quadrantFolder = dir + quadrant + "/"
        try:
            os.mkdir(quadrantFolder)
        except OSError:
            print ("Creation of the directory %s failed" % quadrantFolder)
        else:
            print ("Successfully created the directory %s " % quadrantFolder)

        for audio in os.listdir(dataset + source + "/" + quadrant):

            features, features_frames = es.MusicExtractor(lowlevelStats=lst,
                                                        rhythmStats=lst,
                                                        tonalStats=lst,
                                                        mfccStats=lst,
                                                        gfccStats=lst)(dataset + source + "/" + quadrant + "/" + audio)   

            separation = audio.find(".")
            songName = audio[0:separation]                                          

            es.YamlOutput(filename = quadrantFolder + "/" + songName + ".json", format = 'json')(features)

            for key in features.descriptorNames():
                if "metadata" in key:
                    continue
                elif "rhythm.beats_position" in key:
                    continue
                elif "rhythm.bpm_histogram" in key:
                    continue
                elif isinstance(features[key], numpy.ndarray):
                    for value in features[key]:
                        out.write('%f;' % value)
                elif isinstance(features[key], str):
                    if "scale" in key:
                        out.write('%f;' % scaleNotation(features[key]))
                    else:
                        out.write('%f;' % keyNotation(features[key]))
                else:
                    out.write('%f;' % features[key])
            # quadrant = Q1 / Q2 ...
            txt = quadrant[1:]
            out.write('%s;' % txt)
            out.write("\n")
            print('Music number: %s' % musicNumber)
            musicNumber = musicNumber + 1