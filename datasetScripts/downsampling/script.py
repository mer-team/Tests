import os, os.path
from pydub import AudioSegment

# quadrants
dataset = "/vagrant/dataset/"
output = "/vagrant/datasetFinal/"
counter = 1

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
            # load file
            sound = AudioSegment.from_wav(dataset + source + "/" + quadrant + "/" + audio)
            new_audio = sound.set_frame_rate(22500).set_channels(1)
            # export
            new_audio.export(quadrantFolder + audio, format="wav")
            print(counter)
            counter = counter + 1