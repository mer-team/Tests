# https://api.lyrics.ovh/v1/artist/title
# https://www.youtube.com/watch?v=LC1-VD2eeR0

import requests
import json

artist = "Guns N' Roses"
title = "Sweet Child O' Mine"
url = "https://api.lyrics.ovh/v1/" + artist + "/" + title


response = requests.get(url)
json_data = json.loads(response.content)
lyrics = json_data['lyrics']


print(lyrics)