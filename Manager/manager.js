var amqp = require('amqplib/callback_api');

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
        channel.consume(queue, function (msg) {
            var body = JSON.parse(msg.content);
            console.log(" [x] Received %s", body);

            var service = body.Service;
            var result = body.Result;

            switch(service) {
                case "VidExtractor":
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
                        artist: result.artist
                    };
                    channel.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)));
                    console.log(" [x] Sent %s to %s", toSend, queue);
                  break;
                case "Spleeter":
                    // TO DO
                  break;
                default:
                  // code block
              }
        }, {
            noAck: true
        });
    });
});