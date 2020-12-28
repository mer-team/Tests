# https://lyricsgenius.readthedocs.io/en/master/
import lyricsgenius as lg
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY=os.environ.get("GENIUS_KEY")

genius = lg.Genius(API_KEY,
                    skip_non_songs=True,
                    remove_section_headers=True,
                    excluded_terms = ["(Remix)", "(Live)"])

song = genius.search_song("Alone", "Marshmello")
print(song)
# s = song.save_lyrics(filename="Alone", extension='txt', overwrite='true')


