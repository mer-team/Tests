import os, os.path
from pydub import AudioSegment

# quadrants
dataset = "/vagrant/dataset/"
output = "/vagrant/datasetWav/"
counter = 1

for folder in os.listdir(dataset):
    # create folder to save musics
    dir = output + folder + "/"
    try:
        os.mkdir(dir)
    except OSError:
        print ("Creation of the directory %s failed" % dir)
    else:
        print ("Successfully created the directory %s " % dir)

    for audio in os.listdir(dataset + folder):
        # get only audio name
        separator = audio.find(".")
        audio = audio[0:separator]
        # load file
        sound = AudioSegment.from_mp3(dataset + folder + "/" + audio + ".mp3")
        sound.export(dir + audio + ".wav", format="wav")
        print(counter)
        counter = counter + 1