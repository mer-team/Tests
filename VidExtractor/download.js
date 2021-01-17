const fs = require('fs')
const ytdl = require('ytdl-core')
var ffmpeg = require('fluent-ffmpeg');
var amqp = require('amqplib/callback_api');


/** 
 * Verifica se o URL fornecido está num formato válido aceite pelo Youtube 
 * @param {string} url URL fornecido
 * @returns {boolean}
*/
validURL = async (url) => {
	var result;
	try {
		result = await ytdl.getBasicInfo(url)
		if (result.videoDetails.media.category != "Music") {
			console.log("Not a music")
			return;
		}
	} catch (err) {
		console.log("Not a valid ID, err: " + err)
		return
	}
	return ytdl.validateURL(url);
}

/**
 * Extrai o vídeo correspondente ao URL fornecido
 * @param {string} url URL fornecido
 * @returns {boolean} Resultado da extração, se foi ou não extraído
 */
extractVideo = async (url, ch) => {
	var vID = ytdl.getURLVideoID(url);
	var path = './' + vID + '.mp4'
	var output = './' + vID + '.wav'
	var audio = ytdl(url);

	audio.pipe(fs.createWriteStream(path));
	// sudo apt-get install ffmpeg
	// ffmpeg -i M2EbMpGImMA.wav -ac 1 -ar 22500 mono.wav

	audio.on('end', function () {
		var command = ffmpeg(path)
			.toFormat('wav')
			.on('error', function (err) {
				console.log('An error occurred: ' + err.message);
			})
			.on('end', async function () {
				console.log('Completed video extraction!')
				//get video info
				await ytdl.getBasicInfo(url).then(function (videoInfo, err) {
					if (err) throw new Error(err);

					// console.log(videoInfo.videoDetails.media)
					var media = videoInfo.videoDetails.media;
					var toSend = {
						Service: "VidExtractor",
						Result: {
							"vID": vID,
							"song": media.song,
							"artist": media.artist
						}
					}

					var queue = 'management';
					ch.assertQueue(queue, { durable: false });
					ch.sendToQueue(queue, Buffer.from(JSON.stringify(toSend)), { persistent: false });
					console.log(" [x] Sent '%s' to '%s", toSend, queue);
				});
			})
			.saveToFile(output);
	});
}


/**
 * Inicializa todos os métodos necessários para a validação, extração e conversão de um vídeo para versão áudio
 */
startScript = async () => {
	console.log("Starting")
	amqp.connect('amqp://localhost', function (error0, connection) {
		if (error0) {
			throw error0;
		}
		connection.createChannel(function (error1, channel) {
			if (error1) {
				throw error1;
			}
			// var queue = 'musicExtraction';

			// channel.assertQueue(queue, { durable: false });
			// console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q);
			// ch.consume(q, async function (msg) {
			// 	console.log(" [x] Received %s", msg.content.toString());
			// 	var url = msg.content.toString();
			var url = "https://www.youtube.com/watch?v=ALZHF5UqnU4";
			var vURL = validURL(url).then(u => u)
			if (vURL) {
				extractVideo(url, channel).then();
			}
		}, { noAck: true });
		// });
	});
}

/**
 * Executa o método startScript
 */
startScript();