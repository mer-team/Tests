import pprint
import essentia
import essentia.standard as es
import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='musicFeatures')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    path = '/vagrant/SourceSeparation/Spleeter/Output/' + body.decode("utf-8") + '/'
    featExtracted = []

    # using musics separated with Spleeter 2 stems
    # check the number of songs in the folder
    # divide by 2, where half is vocals and half is accompaniment
    total = len(os.listdir(path))
    # accompaniment
    for i in range(1,int(total/2)):
        music = os.listdir(path)[i]
        features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                    rhythmStats=['mean', 'stdev'],
                                                    tonalStats=['mean', 'stdev'])(path + music)
        featExtracted.append([features['lowlevel.pitch_salience.mean'], features['lowlevel.average_loudness'], features['rhythm.bpm']])

    print(featExtracted)#[[0.4994540810585022, 0.6595611572265625, 142.0624237060547], ..., [0.34013283252716064, 0.9822816252708435, 142.0262451171875]]
    # vocal
    for i in range(int(total/2)+1,total):
        music = os.listdir(path)[i]
        features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                    rhythmStats=['mean', 'stdev'],
                                                    tonalStats=['mean', 'stdev'])(path + music)
        featExtracted.append([features['lowlevel.pitch_salience.mean'], features['lowlevel.average_loudness'], features['rhythm.bpm']])

    print(featExtracted)

    # help(essentia.standard.MusicExtractor)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(sorted(features.descriptorNames())) # See all feature names in the pool in a sorted order
    # print('Number of features:', len(features.descriptorNames())) # 161
    # print('Zero-Crossing Rate: ' + str(features['lowlevel.zerocrossingrate.mean'])) # Another feature extracted

    # print("Filename:", features['metadata.tags.file_name'])
    # print("-" * 80)
    # print("Pitch Salience:")
    # print("                Mean:", features['lowlevel.pitch_salience.mean'])
    # print("                StDev:", features['lowlevel.pitch_salience.stdev'])
    # print("-" * 80)
    # print("Loudness:",features['lowlevel.average_loudness'])
    # print("-" * 80)
    # print("BPM:", features['rhythm.bpm'])
    # print("Beat positions (sec.)", features['rhythm.beats_position'])


channel.basic_consume(queue='musicFeatures',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
