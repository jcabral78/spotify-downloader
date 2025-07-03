import argparse
import os
import json
import lib

caminho_config_api = f"{os.environ['HOME']}/.config/spotify-downloader/api.json"

# Inicialização do parser
parser = argparse.ArgumentParser(prog = "spotify-downloader",
                                 description = "Uma ferramenta CLI que automatiza a instalação e organização de playlists locais usando o spotify.")

# Criação e configuração da flag "config"
parser.add_argument("-c", "--config", type = ascii,
                    nargs = 2, help = "Criar a configuração",
                    metavar = ("client_id", "client_secret"))

# Criação e configuração da flag "album"
parser.add_argument("-a", "--album", type = ascii,
                    help = "Baixar álbuns", metavar = "album_url")

args = parser.parse_args()

if args.config[0] != None and args.config[1] != None:
    lib.criar_config_api(caminho_config_api, args.config[0].replace("'", ""), args.config[1].replace("'", ""))

lib.abrir_config()
lib.criar_pastas()

if args.album != None:
    lib.pegar_album(args.album.replace("'", ""))
else:
    # Baixar músicas pela configuração
    try:
        for musica_config in lib.config["musica"]:
            lib.pegar_musica(musica_config)
    except:
        pass
    lib.pegar_playlists()
    # Baixar álbuns pela configuração
    try:
        for album_config in lib.config["album"]:
            lib.pegar_album(album_config["url"])
    except:
        pass
