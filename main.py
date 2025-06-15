import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import arquivos
import playlist
import album
import outros

caminho_config_home = [
    f"{os.environ['HOME']}/.config/spotify-downloader",
]

id_os_config = {
    "linux": 0
}

# Checa o caminho da configuração
for i in range(len(caminho_config_home)):
    if os.path.isdir(f"{caminho_config_home[i]}"):
        caminho_config = f"{caminho_config_home[i]}/config.json"
        caminho_config_api = f"{caminho_config_home[i]}/api.json"
        break

# Abre o arquivo de configuração
try:
    with open(caminho_config) as arquivo_config:
        config = json.load(arquivo_config)
except:
    arquivos.criar_config(caminho_config_home)

# Abre o arquivo de configuração da API
try:
    with open(caminho_config_api) as arquivo_config_api:
        config_api = json.load(arquivo_config_api)
except:
    arquivos.criar_config_api(caminho_config_home[id_os_config[config["OS"]]])

# Checa o objeto "OS" na configuração e dá valores a variáveis de acordo com o valor do mesmo
match config["OS"]:
    case "linux":
        caminho_arquivo_inicio = os.environ['HOME']
    case _:
        print("Erro na config: OS")
        exit(0)

match config["OS"]:
    case "linux":
        cache = f"{caminho_arquivo_inicio}/.cache/spotifyAPItoken"

# Setup da API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config_api["client_id"],
                                               client_secret=config_api["client_secret"],
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="playlist-read-private",
                                               cache_path=cache))

arquivos.criar_pastas(caminho_arquivo_inicio)

print("O que você quer baixar?")
print("1) Álbum")
print("2) Outros")
opcao = int(input())

match opcao:
    case 1:
        url = input("Escreva o URL de um álbum: ")
        album.baixar_album(sp, config, caminho_arquivo_inicio, url)

    case 2:
        # Baixar músicas pela configuração
        try:
            for musica_config in config["musica"]:
                outros.baixar_musica(sp, config, caminho_arquivo_inicio, musica_config)
        except:
            pass

        playlist.baixar_playlists(sp, config, caminho_arquivo_inicio)

        # Baixar álbuns pela configuração
        try:
            for album_config in config["album"]:
                url = album_config["url"]
                album.baixar_album(sp, config, caminho_arquivo_inicio, url)
        except:
            pass

    case _:
        print("Erro de input")
