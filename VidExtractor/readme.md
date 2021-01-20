# Obtain the video file to be processed using [node-ytdl-core](https://www.npmjs.com/package/ytdl-core).

This service is connected with ['Manager'](https://github.com/mer-team/Tests/blob/rabbit-manager/Manager/manager.js) service through [RabbitMQ](https://www.rabbitmq.com/). 
Checks if the video to be processed is categorized as music. If so, the video is downloaded, converted to .wav format and saved.


Run `node download.js`

## Input through RabbitMQ

The input is the URL of the youtube video.

## Output

Audio file for further processing. The name of that file is his youtube ID.

Through RabbitMQ:
```javascript
If this video isn't categorized as music:
{ Service: 'VidExtractor', Result: 'Not a music' }

                       OR                       

If song and artist are identified with success:
{ Service: 'VidExtractor', Result: { vID: 'vID', Song: 'Song name', Artist: 'Artist name' } }

                                             OR                                              

If song and artist aren't identified with success:
{ Service: 'VidExtractor', Result: { vID: 'vID' } }
```

---

# Segment and downsampling of audio files returned by Spleeter using [fluent-ffmpeg](https://www.npmjs.com/package/fluent-ffmpeg).

This service is connected with ['Manager'](https://github.com/mer-team/Tests/blob/rabbit-manager/Manager/manager.js) service through [RabbitMQ](https://www.rabbitmq.com/). 
Segments an audio file into smaller files with 30 seconds length and 15 seconds of overlapping. This files are saved with one audio channel only and 22500 Hz of frequency.

Run `node segmentation.js`

## Input through RabbitMQ

The input is the videoID which is the folder that contains separate audio files.

## Output

Segmented audio files.

Through RabbitMQ:
```javascript
{ Service: 'Segmentation', Result: { vID: 'vID' } }
```
---
# Other scripts
## details.js

Read metadata from any valid ffmpeg input file.

## downsampling.js

Allows to modify the number of audio channels and audio frequency.