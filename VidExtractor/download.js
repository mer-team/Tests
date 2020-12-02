const fs = require('fs')
const ytdl = require('ytdl-core')
var ffmpeg = require('fluent-ffmpeg');
var url = "https://www.youtube.com/watch?v=ALZHF5UqnU4";

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
		.on('error', function(err) {
			console.log('An error occurred: ' + err.message);
		})
		.on('end', function () {
			console.log('Processing finished!')
		})
		.saveToFile(output);
});
