import nussl 
from time import perf_counter

path = "song.wav"

mixture = nussl.AudioSignal(path)

# print(mixture.audio_data.shape) #number of channels and samples
t1_start = perf_counter()  

separator = nussl.separation.primitive.FT2D(mixture)
estimates = separator()

t1_stop = perf_counter() 
  
background = estimates[0]
foreground =  estimates[1]
print(background)
print(foreground)
print("Elapsed time in seconds:", t1_stop-t1_start) 
print("Duration: {} seconds".format(background.signal_duration))
print("Duration in samples: {} samples".format(background.signal_length))
print("Number of channels: {} channels".format(background.num_channels))
print("File name: {}".format(background.file_name))
print("Root mean square energy: {:.4f}".format(background.rms().mean()))
