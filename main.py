import argparse
import os
import json
import sys
import lib

lib.checar_sistema()

# Inicialização do parser
parser = argparse.ArgumentParser(prog = "spotify-downloader",
                                 description = "Uma ferramenta CLI que automatiza a instalação e organização de playlists locais usando o spotify.")

# Criação e configuração da flag "config"
parser.add_argument("-c", "--config", nargs = 2,
                    help = "Criar a configuração", metavar = ("navegador", "imagens"))

# Criação e configuração da flag "config-api"
parser.add_argument("-C", "--config-api", type = ascii,
                    nargs = 2, help = "Criar a configuração da API",
                    metavar = ("client_id", "client_secret"))


# Criação e configuração da flag "album"
parser.add_argument("-a", "--album", type = ascii,
                    help = "Baixar álbuns", metavar = "album_url")

# Processamento dos argumentos
args = parser.parse_args()

if args.config_api != None: 
    lib.criar_config_api(args.config_api[0].replace("'", ""), args.config_api[1].replace("'", ""))

if args.config != None:
    if args.config[0].lower() in ("nenhum", "null", "none"):
        args.config[0] = None
    else:
        args.config[0] = args.config[0].lower().replace("'", "")
    
    if args.config[1].lower() in ("sim", "true"):
        args.config[1] = True
    elif args.config[1].lower() in ("nao", "não", "false"):
        args.config[1] = False
    else:
        print("Erro no input")
        sys.exit(0)

    lib.criar_config(args.config[0], args.config[1])

lib.abrir_config()
lib.criar_pastas()

if not "navegador" in lib.config:
    print("Erro na config: navegador")
    sys.exit(0)

if not "imagens" in lib.config:
    print("Erro na config: imagens")
    sys.exit(0)

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
