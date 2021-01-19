# Obtain Music Genre with [Last.fm API](https://www.last.fm/api)

This service is connected with ['Manager'](https://github.com/mer-team/Tests/blob/rabbit-manager/Manager/manager.js) service through [RabbitMQ](https://www.rabbitmq.com/). Get the five most suitable music genres for each song.

Run `python3.7 last_fm.py`

## Input through RabbitMQ

```javascript
{ song: 'Track Name', artist: 'Artist Name' }
                     OR                      
{ song: 'Undefined', artist: 'Undefined' }
```

## Output
There is an error in the procedure of obtaining the musical genres:
```javascript
{ Service: 'GenreFinder', Error : 'True', Result: 'Error message' }

```

Obtaining the musical genres succeed:
```javascript
{ Service: 'GenreFinder', Error : 'False', Result: 'Genres' }

```