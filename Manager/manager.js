var amqp = require('amqplib/callback_api');
const fs = require('fs');
const { orderBy } = require('natural-orderby');
const MongoClient = require('mongodb').MongoClient
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
                    case "VidExtractor":
                        if (result == "Not a music") {
                            console.log("Not Music. Ending!")
                        } else {
                            // INSERT ONE DOCUMENT INTO DB
                            const doc = {
                                videoID: result.vID, song: result.song, artist: result.artist,
                                accompaniment: [], original: [], vocals: []
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
                            var toSend = {
                                vID: result.vID,
                                path: relativedir,
                                source: file.substring(0, pos)
                            }
                            channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                        }
                        console.log(" [x] Sent %s to %s", "Segmented files", queue);
                        break;
                    case "AudioFeaturesExtractor":
                        if (result.error != undefined) {
                            console.log(result.error)
                            // TODO
                        } else {
                            let query = {}
                            query[result.source] = result.featExtracted;
                            let append = { $push: query };
                            await collection.findOneAndUpdate({ videoID: result.vID }, append);
                        }
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
                            // TO DO - END?
                        } else {
                            // UPDATE DOCUMENT 
                            let lyrics = { $set: { lyrics: result.Lyrics } };
                            await collection.updateOne({ videoID: result.videoID }, lyrics);
                            // TO DO - CALL FEATURE EXTRACTION
                        }
                        break;
                    default:
                    // code block
                }
            }, {
                noAck: true
            });
        });
    });
}

run();