var ffmpeg = require('fluent-ffmpeg');
var amqp = require('amqplib/callback_api');

segmentation = async (channel, vID, audio) => {
    var path = "/vagrant/SourceSeparation/Spleeter/Output/" + vID + "/";
    // file metadata
    ffmpeg.ffprobe(path + audio + '.wav', async function (err, metadata) {
        var inputSec = 0;
        var duration = metadata.format.duration;
        // Round a number upward to its nearest integer:
        var nFiles = Math.ceil(duration / 15); // overlap 15 seconds
        for (let i = 1; i <= nFiles; i++) {
            var command = ffmpeg(path + audio + '.wav')
                .seekInput(inputSec)
                .duration(30)
                .withAudioChannels(1)
                .withAudioFrequency(22500)
                .on('error', function (err) {
                    console.log('An error occurred: ' + err.message);
                })
                .on('end', function () {
                    // true when i is the last file and audio is vocals
                    // so it just trigger once
                    if (i == nFiles && audio == "vocals") {
                        var q = 'management';
                        var toSend = {
                            Service: "Segmentation",
                            Result: { "vID": vID }
                        }
                        channel.sendToQueue(q, Buffer.from(JSON.stringify(toSend)));
                        console.log(" [x] Sent %s to %s", toSend, q);
                    }
                })
                .saveToFile(path + audio + "_" + i + ".wav");

            inputSec = inputSec + 15;
        }
    });
}

amqp.connect('amqp://localhost', async function (error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(async function (error1, channel) {
        if (error1) {
            throw error1;
        }
        var queue = 'segmentation';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
        channel.consume(queue, function (msg) {
            var vID = msg.content.toString()
            console.log(" [x] Received %s", vID);
            //using source separation with 2 stems (vocals and accompaniment)
            let sourceType = ['accompaniment', 'original', 'vocals']
            for (let index = 0; index < sourceType.length; index++) {
                segmentation(channel, vID, sourceType[index]);
            }
        }, {
            noAck: true
        });
    });
});
