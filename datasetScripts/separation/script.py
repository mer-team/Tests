from spleeter.separator import Separator
import os

def createFolder(dir):
    try:
        os.mkdir(dir)
    except OSError:
        print ("Creation of the directory %s failed" % dir)
    else:
        print ("Successfully created the directory %s " % dir)

# quadrants
dataset = "/vagrant/datasetWav/originalSongs/"
accompanimentSongs = "/vagrant/datasetWav/accompanimentSongs/"
vocalSongs = "/vagrant/datasetWav/vocalSongs/"
counter = 1

# Using embedded configuration.
separator = Separator('spleeter:2stems')
# separator = Separator('spleeter:4stems')

for folder in os.listdir(dataset):
    createFolder(accompanimentSongs + folder)
    createFolder(vocalSongs + folder)

    for audio in os.listdir(dataset + folder):
        separator.separate_to_file(dataset + folder + "/" + audio, "./")

        separation = audio.find(".")
        song = audio[0:separation]

        # # Move a file by renaming it's path
        os.rename("./" + song + "/accompaniment.wav", accompanimentSongs + folder + "/" +  audio)
        os.rename("./" + song + "/vocals.wav", vocalSongs + folder + "/" +  audio)
        os.rmdir("./" + song)
        print(counter)
        counter = counter + 1


