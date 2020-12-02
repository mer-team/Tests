var ffmpeg = require('fluent-ffmpeg');

var audio = 'ALZHF5UqnU4.wav';
var duration; // file duration in seconds
var nFiles; //number of files needed
var inputSec=0;

// file metadata
ffmpeg.ffprobe(audio, function (err, metadata) {
    duration = metadata.format.duration;
    // Round a number upward to its nearest integer:
    nFiles = Math.ceil(duration / 15);
    // console.log(nFiles)
    for (let i = 1; i <= nFiles; i++) {
        var command = ffmpeg(audio)
        .seekInput(inputSec)
        .duration(30)
        .withAudioChannels(1)
        .withAudioFrequency(22500)
        .on('error', function(err) {
            console.log('An error occurred: ' + err.message);
        })
        .on('end', function () {
            // console.log('Processing finished!')
        })
        .saveToFile(i + "_" + audio) 

        inputSec = inputSec + 15;
    }
});




