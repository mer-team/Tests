#install requirements -> pip3 install --user -r requirements.txt
import json
import pika
from joblib import load

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='classifyMusic')
channel.queue_declare(queue='management')

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    # print received message
    print(" [x] Received Features")
    b = json.loads(body.decode('utf-8'))
    source = b['source']
    features = b['features']
    vID = b['vID']

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
        if source == 'emotions_accompaniment':
            print('acompanhamento')
            # clf = load('trainedModel.joblib')
            # scaler = load('scaler.joblib')
        if source == 'emotions_original':
            print('original')
            # clf = load('trainedModel.joblib')
            # scaler = load('scaler.joblib')
        if source == 'emotions_vocals':
            # clf = load('trainedModel.joblib')
            # scaler = load('scaler.joblib')
            print("vocals")
        if source == 'emotions_allaudio':
            # clf = load('trainedModel.joblib')
            # scaler = load('scaler.joblib')
            print("allaudio")

    # name = b[0].split(".")[0]
    # toTest = [b[1],b[2],b[3]]
    # ft = scaler.transform([toTest])
    # p = clf.predict(ft)
    # print("Predict = ", p)
    # emotion = ""
    # if p == "1":
    #     emotion = "Feliz"
    # if p == "2":
    #     emotion = "Tensa"    
    # if p == "3":
    #     emotion = "Triste"   
    # if p == "4":
    #     emotion = "Calma"
    # r = requests.post("https://merapi.herokuapp.com/music/update", {'idVideo': name, 'emocao': emotion})
    # print(r.status_code, r.reason)
    # print(' [*] Waiting for messages. To exit press CTRL+C')


channel.basic_consume(queue='classifyMusic',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()