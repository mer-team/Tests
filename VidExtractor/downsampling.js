var ffmpeg = require('fluent-ffmpeg');

var audio = 'ALZHF5UqnU4.wav';

var output = 'v2' + audio

var command = ffmpeg(audio)
    .withAudioChannels(1)  // Specify the number of audio channels
    .withAudioFrequency(22500)
    .on('error', function(err) {
        console.log('An error occurred: ' + err.message);
    })
    .on('end', function () {
        console.log('Processing finished!')
    })
    .saveToFile(output);
