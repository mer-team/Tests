import requests
import os
import pika
import json
from dotenv import load_dotenv
load_dotenv()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='genre')

def callback(ch, method, properties, body):
    info = json.loads(body.decode('utf-8'))
    print(" [x] Received %r" % info)

    # create URL
    urlRoot = "http://ws.audioscrobbler.com/2.0/?"
    method = "track.getinfo"
    LAST_FM_KEY=os.environ.get("LAST_FM_KEY")
    artist = info['artist']
    track = info['song']

    url = urlRoot + "method=" + method + "&api_key=" + LAST_FM_KEY + "&artist=" + artist + "&track=" + track + "&format=json"

    req = requests.get(url).json()
    # CHECK IF THERE IS A 'ERROR' KEY IN THE RESULT
    if "error" in req:
        msg = {
            "Service": "GenreFinder",
            "Error" : "True",
            "Result": req['message']
        }

        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)
    else:
        toptags = req['track']['toptags']['tag']
        genres = ""

        for value in toptags:
            genres = genres + value['name'] + ", "

        genres = genres[:-2]

        msg = {
            "Service": "GenreFinder",
            "Error" : "False",
            "Result": genres
        }
        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)

channel.basic_consume(queue='genre',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()