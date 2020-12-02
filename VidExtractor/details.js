var ffmpeg = require('fluent-ffmpeg');

var audio = 'ALZHF5UqnU4.wav';

// read metadata
ffmpeg.ffprobe(audio, function (err, metadata) {
    console.dir(metadata);
});
