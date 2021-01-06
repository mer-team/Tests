from spleeter.separator import Separator

from time import perf_counter #from https://www.geeksforgeeks.org/time-perf_counter-function-in-python/

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='segmentation')

# Using embedded configuration.
separator = Separator('spleeter:2stems')
# separator = Separator('spleeter:4stems')

audio="song.wav"
destination="./Output"

# Start the stopwatch / counter 
t1_start = perf_counter()  

separator.separate_to_file(audio, destination)

# Stop the stopwatch / counter 
t1_stop = perf_counter() 
  
  
print("Elapsed time in seconds:", t1_stop-t1_start) 

channel.basic_publish(exchange='',
                      routing_key='segmentation',
                      body=audio[:-4])
print(" [x] Sent " + audio)


# spleeter separate -i song.wav -o ./Output -p spleeter:2stems