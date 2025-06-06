import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from arquivos import config

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["client_id"],
                                               client_secret=config["client_secret"],
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="playlist-read-private",
                                               cache_path=f"{os.environ['HOME']}/.cache/.spotifyAPItoken"))
