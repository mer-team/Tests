import requests
import os
from dotenv import load_dotenv
load_dotenv()

LAST_FM_KEY=os.environ.get("LAST_FM_KEY")

artist = "Guns N' Roses"
track = "Sweet Child O' Mine"
url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + LAST_FM_KEY + "&artist=" + artist + "&track=" + track + "&format=json"

req = requests.get(url).json()
toptags = req['track']['toptags']['tag']
genres = ""

for value in toptags:
    genres = genres + value['name'] + ", "

genres = genres[:-2]

print(genres)