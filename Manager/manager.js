var amqp = require('amqplib/callback_api');
const fs = require('fs');
const { orderBy } = require('natural-orderby');
const MongoClient = require('mongodb').MongoClient
const axios = require('axios')
// path onde estao as musicas segmentadas
var path = '/vagrant/SourceSeparation/Spleeter/Output/'

const url = 'mongodb://localhost:27017/'
let db
let res;
let collection;

run = async () => {
    try {
        // CONNECTION
        db = await MongoClient.connect(url)
        console.log('Connected successfully!')
        // USE DATABASE MUSIC
        var dbo = db.db('music');
        // USE COLLECTION MUSIC
        collection = dbo.collection('music')

    } catch (error) {
        // Handle error
        console.log(error);
    }

    amqp.connect('amqp://localhost', function (error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function (error1, channel) {
            if (error1) {
                throw error1;
            }
            var queue = 'management';
            channel.assertQueue(queue, {
                durable: false
            });
            console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
            channel.consume(queue, async function (msg) {

                try {
                    var body = JSON.parse(msg.content);
                    if (typeof body == 'string') {
                        console.log(" [x] Received Features")
                    } else {
                        console.log(" [x] Received %s", body);
                    }
                    var service = body.Service;
                    var result = body.Result;
                    if (service == undefined || result == undefined) {
                        body = body.replace(/'/g, '"');
                        body = JSON.parse(body);
                        service = body.Service;
                        result = body.Result;
                    }
                    switch (service) {
                        case "API":
                            var q = 'musicExtraction';
                            channel.assertQueue(q, {
                                durable: false
                            });
                            const url = result.url;
                            channel.sendToQueue(q, Buffer.from(url));
                            console.log(" [x] Sent %s to %s", url, q);
                            break;
                        case "VidExtractor":
                            if (result == "Not a music") {
                                console.log("Not Music. Ending!")
                            } else {
                                // INSERT ONE DOCUMENT INTO DB
                                const doc = {
                                    videoID: result.vID, song: result.song, artist: result.artist,
                                    accompaniment: [], original: [], vocals: [], emotions_accompaniment: [],
                                    emotions_original: [], emotions_vocals: [], emotions_allaudio: [], emotions_lyrics: []
                                };
                                await collection.insertOne(doc).then(res => res = res);

                                // SOURCE SEPARATION
                                var queue = 'separate';
                                channel.assertQueue(queue, {
                                    durable: false
                                });
                                var vID = result.vID;
                                channel.sendToQueue(queue, Buffer.from(vID));
                                console.log(" [x] Sent %s to %s", vID, queue);
                                // LYRICS
                                queue = 'lyrics';
                                channel.assertQueue(queue, {
                                    durable: false
                                });
                                var toSend = {
                                    song: result.song,
                                    artist: result.artist,
                                    vID: result.vID
                                };
                                channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                console.log(" [x] Sent %s to %s", toSend, queue);
                                // GENRE
                                queue = 'genre';
                                channel.assertQueue(queue, {
                                    durable: false
                                });
                                var toSend = {
                                    song: result.song,
                                    artist: result.artist,
                                    vID: result.vID
                                };
                                channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                console.log(" [x] Sent %s to %s", toSend, queue);
                            }
                            break;
                        case "SourceSeparation":
                            var queue = 'segmentation';
                            channel.assertQueue(queue, {
                                durable: false
                            });
                            var vID = result.vID;
                            channel.sendToQueue(queue, Buffer.from(vID));
                            console.log(" [x] Sent %s to %s", vID, queue);
                            break;
                        case "Segmentation":
                            let numFiles = { $set: { numFiles: result.numFiles } };
                            await collection.updateOne({ videoID: result.vID }, numFiles);
                            // read directory
                            let files = orderBy(fs.readdirSync(path + result.vID))
                            for (let index = 0; index < files.length; index++) {
                                const file = files[index];
                                // discard accompaniment, original, vocals
                                if (!file.includes("_")) {
                                    continue
                                }
                                let relativedir = result.vID + "/" + file;
                                let pos = file.indexOf("_");
                                var queue = 'musicFeatures';
                                channel.assertQueue(queue, {
                                    durable: false
                                });
                                if (index != (files.length - 1)) {
                                    var toSend = {
                                        vID: result.vID,
                                        path: relativedir,
                                        source: file.substring(0, pos),
                                        last: 'False'
                                    }
                                } else {
                                    var toSend = {
                                        vID: result.vID,
                                        path: relativedir,
                                        source: file.substring(0, pos),
                                        last: 'True'
                                    }
                                }
                                channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                            }
                            console.log(" [x] Sent %s to %s", "Segmented files", queue);
                            break;
                        case "AudioFeaturesExtractor":
                            let query = {}
                            if (result.error != undefined) {
                                console.log(result.error)
                                query[result.source] = result.error;
                                // TODO IN CASE OF ERROR / SILENT FILE
                            } else {
                                query[result.source] = result.featExtracted;
                            }
                            let append = { $push: query };
                            await collection.findOneAndUpdate({ videoID: result.vID }, append);

                            if (result.last == 'True') {
                                // get all features to classify
                                let musicRecord;
                                await collection.findOne({ videoID: result.vID }).then(res => musicRecord = res);
                                // example 
                                // {
                                //     videoID: 'ALZHF5UqnU4',
                                //     song: 'Alone',
                                //     artist: 'Marshmello',
                                //     accompaniment: [],
                                //     original: [],
                                //     vocals: [],
                                //     numFiles: 14
                                //   }
                                let numFiles = musicRecord.numFiles;
                                var queue = 'classifyMusic';
                                channel.assertQueue(queue, {
                                    durable: false
                                });
                                var toSend = {};
                                for (let index = 0; index < numFiles; index++) {
                                    // classify accompaniment, original, vocal, allcombined
                                    // accompaniment
                                    toSend = {
                                        vID: result.vID,
                                        features: musicRecord.accompaniment[index],
                                        source: 'emotions_accompaniment',
                                        last: 'False'
                                    }

                                    channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                    console.log(" [x] Sent %s to %s", `Features of accompaniment[${index}]`, queue);
                                    // original
                                    toSend = {
                                        vID: result.vID,
                                        features: musicRecord.original[index],
                                        source: 'emotions_original',
                                        last: 'False'
                                    }
                                    channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                    console.log(" [x] Sent %s to %s", `Features of original[${index}]`, queue);
                                    // vocals
                                    toSend = {
                                        vID: result.vID,
                                        features: musicRecord.vocals[index],
                                        source: 'emotions_vocals',
                                        last: 'False'
                                    }
                                    channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                    console.log(" [x] Sent %s to %s", `Features of vocals[${index}]`, queue);
                                    // allcombined
                                    let last;
                                    if (index == (numFiles - 1)) {
                                        last = 'True';
                                    } else {
                                        last = 'False'
                                    }
                                    if (typeof musicRecord.accompaniment[index] == 'string' ||
                                        typeof musicRecord.original[index] == 'string' ||
                                        typeof musicRecord.vocals[index] == 'string') {
                                        toSend = {
                                            vID: result.vID,
                                            features: "error",
                                            source: 'emotions_allaudio',
                                            last: last
                                        }
                                    } else {
                                        const merged = Object.assign({}, musicRecord.accompaniment[index],
                                            musicRecord.original[index], musicRecord.vocals[index])
                                        toSend = {
                                            vID: result.vID,
                                            features: merged,
                                            source: 'emotions_allaudio',
                                            last: last
                                        }
                                    }
                                    channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                    console.log(" [x] Sent %s to %s", `Features of vocals[${index}]`, queue);
                                }
                            }
                            break;
                        case "GenreFinder":
                            // UPDATE DOCUMENT
                            let genre = { $set: { genre: result.Result } };
                            await collection.updateOne({ videoID: result.videoID }, genre);
                            break;
                        case "LyricsExtractor":
                            if (result.Filename == "Music Not Found") {
                                // UPDATE DOCUMENT
                                let lyrics = { $set: { lyrics: result.Filename } };
                                await collection.updateOne({ videoID: result.videoID }, lyrics)
                            } else {
                                // UPDATE DOCUMENT 
                                let lyrics = { $set: { lyrics: result.Lyrics } };
                                await collection.updateOne({ videoID: result.videoID }, lyrics);
                                var queue = 'lyricsFeatures';
                                channel.assertQueue(queue, {
                                    durable: false
                                });

                                let toSend = {
                                    vID: result.videoID,
                                    filename: result.Filename,
                                }
                                channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                                console.log(" [x] Sent %s to %s", toSend, queue);

                            }
                            break;
                        case "LyricsFeaturesExtractor":
                            let insert = { $set: { lyricsFeatures: result.features } };
                            await collection.updateOne({ videoID: result.vID }, insert);
                            var queue = 'classifyMusic';
                            channel.assertQueue(queue, {
                                durable: false
                            });
                            toSend = {
                                vID: result.vID,
                                features: result.features,
                                source: 'emotions_lyrics',
                                last: 'False'
                            }
                            channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                            console.log(" [x] Sent Features of Lyrics to %s", queue);
                            break
                        case "Classifier":
                            let queryClassifier = {}
                            queryClassifier[result.source] = result.emotion;
                            let appendClassifier = { $push: queryClassifier };
                            await collection.findOneAndUpdate({ videoID: result.vID }, appendClassifier);
                            if (result.last == 'True') {
                                let musicRecord;
                                await collection.findOne({ videoID: result.vID }).then(res => musicRecord = res);
                                const toSendAPI = {
                                    'videoID': musicRecord.videoID, 'accompaniment': musicRecord.emotions_accompaniment,
                                    'original': musicRecord.emotions_original, 'vocals': musicRecord.emotions_vocals,
                                    'allaudio': musicRecord.emotions_allaudio, 'lyrics': musicRecord.emotions_lyrics
                                }
                                axios.post('http://localhost:8000/music/update', toSendAPI)
                                    .then(function (response) { console.log('Success'); })
                                    .catch(function (error) { console.log(error); });
                            }
                            break;
                        default:
                        // code block
                    }
                } catch (error) {
                    console.log(error)
                }
            }, {
                noAck: true
            });
        });
    });
}

run();