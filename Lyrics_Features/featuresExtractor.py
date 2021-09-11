import subprocess
import pandas as pd
import pika
import json
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='lyricsFeatures')
channel.queue_declare(queue='management')

dataset_path = '/vagrant/Lyrics/'

def callback(ch, method, properties, body):
    body = json.loads(body.decode('utf-8'))
    print(" [x] Received %r" % body)

    filename = body['filename']
    file = dataset_path + filename
    # USE  subprocess.run TO GET OUTPUT
    result = subprocess.check_output(['java', '-jar', 'MainInterface.jar', 'all_features', file, 'output.csv']) 

    # read csv
    csv = pd.read_csv('./output.csv', sep = ",", index_col=False)
    csv = csv.drop(['Id'], axis=1)
    features = {}

    for feature in csv.columns:
        value = csv[feature].to_string(index=False)
        if value == 'NaN':
            value = 0
        features[feature] = value

    msg = {
        "Service": "LyricsFeaturesExtractor",
        "Result": { "vID": body['vID'], "features": features}
    }

    channel.basic_publish(exchange='',
                    routing_key='management',
                    body=json.dumps(msg))
    print(" [x] Sent Features of %s to management" % body['vID'])


channel.basic_consume(queue='lyricsFeatures',
                    auto_ack=True,
                    on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
