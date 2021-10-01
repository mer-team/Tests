#install requirements -> pip3 install --user -r requirements.txt
import json
import pika
from joblib import load

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='classifyMusic')
channel.queue_declare(queue='management')

classifiers_path = './classifiers/'

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    # print received message
    print(" [x] Received Features")
    b = json.loads(body.decode('utf-8'))
    source = b['source']
    features = b['features']
    vID = b['vID']
    last = b['last']

    if 'error' in features:
        msg = {
            "Service": "Classifier",
            "Result": { "vID": vID, "source": source, "emotion": "Cannot get emotion" }
        }

        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)
    else:

        # LOAD FEATURES
        features_to_use=open('./features_to_use.json')
        features_to_use = json.load(features_to_use)

        # ACCOMPANIMENT
        if source == 'emotions_accompaniment':
            clf = load( classifiers_path + 'accompaniment_model.joblib')
            scaler = load(classifiers_path + 'accompaniment_scaler.joblib')
            features_to_use = features_to_use['accompaniment']

        # ORIGINAL
        if source == 'emotions_original':
            clf = load( classifiers_path + 'original_model.joblib')
            scaler = load(classifiers_path + 'original_scaler.joblib')
            features_to_use = features_to_use['original']

        # VOCALS
        if source == 'emotions_vocals':
            clf = load( classifiers_path + 'vocal_model.joblib')
            scaler = load(classifiers_path + 'vocal_scaler.joblib')
            features_to_use = features_to_use['vocals']
        # ALL AUDIO
        if source == 'emotions_allaudio':
            clf = load( classifiers_path + 'allaudio_model.joblib')
            scaler = load(classifiers_path + 'allaudio_scaler.joblib')
            features_to_use = features_to_use['allaudio']

        # LYRICS
        if source == 'emotions_lyrics':
            clf = load( classifiers_path + 'lyrics_model.joblib')
            scaler = load(classifiers_path + 'lyrics_scaler.joblib')
            features_to_use = features_to_use['lyrics']

        to_classify = []
        for feature in features_to_use:
            to_classify.append(features[feature])

        ft = scaler.transform([to_classify])
        p = clf.predict(ft)
        # p is array with one value in first position with result from predict
        emotion = str(p[0])

        msg = {
            "Service": "Classifier",
            "Result": { "vID": vID, "source": source, "emotion": emotion, "last": last }
        }

        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)



channel.basic_consume(queue='classifyMusic',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()