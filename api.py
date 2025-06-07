import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from arquivos import config, caminho_arquivo_inicio

match config["OS"]:
    case "linux":
        cache = f"{caminho_arquivo_inicio}/.cache/.spotifyAPItoken"
    case "android":
        cache = f"{caminho_arquivo_inicio}/Músicas/.spotifyAPItoken"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["client_id"],
                                               client_secret=config["client_secret"],
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="playlist-read-private",
                                               cache_path=cache))
