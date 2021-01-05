var ffmpeg = require('fluent-ffmpeg');

// var audio = 'ALZHF5UqnU4.wav';
var duration; // file duration in seconds
var nFiles; //number of files needed
var inputSec=0;

//using source separation with 2 stems (vocals and accompaniment) 
var path = "/vagrant/SourceSeparation/Spleeter/Output/song/"

// file metadata
ffmpeg.ffprobe(path + "vocals.wav", function (err, metadata) {
    duration = metadata.format.duration;
    // Round a number upward to its nearest integer:
    nFiles = Math.ceil(duration / 15);
    // console.log(nFiles)
    for (let i = 1; i <= nFiles; i++) {
        var command = ffmpeg(path + "vocals.wav")
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
        .saveToFile(path + "vocals_" + i + ".wav");

        inputSec = inputSec + 15;
    }
});

// file metadata
ffmpeg.ffprobe(path + "accompaniment.wav", function (err, metadata) {
    duration = metadata.format.duration;
    // Round a number upward to its nearest integer:
    nFiles = Math.ceil(duration / 15);
    // console.log(nFiles)
    for (let i = 1; i <= nFiles; i++) {
        var command = ffmpeg(path + "accompaniment.wav")
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
        .saveToFile(path + "accompaniment_" + i + ".wav");

        inputSec = inputSec + 15;
    }
});



