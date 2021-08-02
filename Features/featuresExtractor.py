import essentia
import essentia.standard as es
import pika
import json
import numpy

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='musicFeatures')
channel.queue_declare(queue='classifyMusic')

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


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    body = json.loads(body.decode('utf-8'))

    path = '/vagrant/SourceSeparation/Spleeter/Output/' + body['path']
    lst = ["min", "max", "median", "mean", "var", "skew", "kurt", "dmean", "dvar", "dmean2", "dvar2"]

    try:
        features, features_frames = es.MusicExtractor(lowlevelStats=lst, rhythmStats=lst, tonalStats=lst, mfccStats=lst,
                                                    gfccStats=lst)(path)  
                                                    
        featExtracted = {}
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
                    key1 = key.replace('.', '_')
                    txt = key1 + "[" + str(counter) + ']_' + body['source']
                    featExtracted[txt] = value
                    counter = counter + 1
            elif isinstance(features[key], str):
                key1 = key.replace('.', '_')
                if "scale" in key:
                    featExtracted[key1 + '_' + body['source']] = scaleNotation(features[key])
                else:
                    featExtracted[key1 + '_' + body['source']] = keyNotation(features[key])
            else:
                key1 = key.replace('.', '_')
                featExtracted[key1 + '_' + body['source']] = features[key]
                
        toSend = {
            "Service": "AudioFeaturesExtractor",
            "Result": { 
                "featExtracted": featExtracted,
                "source": body['source'],
                "vID": body['vID']
            }
        }
        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(str(toSend)))
        print(" [x] Sent ", "Features", " to Manager!!")

    except Exception as error:
        print(error)
        toSend = {
            "Service": "AudioFeaturesExtractor",
            "Result": { 
                "error": "error occurred or file might be silent"
            }
        }
        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(toSend))
        print(" [x] Sent ", json.dumps(toSend), " to Manager!!")



channel.basic_consume(queue='musicFeatures',
                    auto_ack=True,
                    on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
