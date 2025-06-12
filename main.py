import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import arquivos
import playlist
import album

caminho_config = ""
caminho_config_todos = [
    f"{os.environ['HOME']}/.config/spotify-downloader",
]

for i in range(len(caminho_config_todos)):
    if os.path.isfile(f"{caminho_config_todos[i]}/config.json"):
        caminho_config = f"{caminho_config_todos[i]}/config.json"
        break

try:
    with open(caminho_config) as arquivo_config:
        config = json.load(arquivo_config)
except:
    arquivos.criar_config(caminho_config, caminho_config_todos)

match config["OS"]:
    case "linux":
        caminho_arquivo_inicio = os.environ['HOME']
    case _:
        print("Erro na config: OS")
        exit(0)

match config["OS"]:
    case "linux":
        cache = f"{caminho_arquivo_inicio}/.cache/spotifyAPItoken"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["client_id"],
                                               client_secret=config["client_secret"],
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="playlist-read-private",
                                               cache_path=cache))

arquivos.criar_pastas(caminho_arquivo_inicio)

print("O que você quer baixar?")
print("1) Álbum")
print("2) Playlist")
opcao = int(input())

match opcao:
    case 1:
        url = input("Escreva o URL de um álbum: ")
        album.baixar_album(sp, config, caminho_arquivo_inicio, url)

    case 2:
        playlist.baixar_playlists(sp, config, caminho_arquivo_inicio)

    case _:
        print("Erro de input")
