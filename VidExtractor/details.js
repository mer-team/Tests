var ffmpeg = require('fluent-ffmpeg');

// SONG NAME
var audio = 'ALZHF5UqnU4.wav';

// read metadata
ffmpeg.ffprobe(audio, function (err, metadata) {
    console.dir(metadata);
});
