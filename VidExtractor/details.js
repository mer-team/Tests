var ffmpeg = require('fluent-ffmpeg');

// SONG NAME
var audio = "/vagrant/datasetFinal/originalSongs/Q3/MT0001193971.wav";

// read metadata
ffmpeg.ffprobe(audio, function (err, metadata) {
    console.dir(metadata);
});
