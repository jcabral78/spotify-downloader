import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TRCK, APIC
import os
import json
import requests
import sys
import platform

# Checa se o sistema é Windows ou Linux e define variáveis globais
def checar_sistema():
    global caminho_inicio
    global caminho_config
    global caminho_cache

    if platform.system().lower() == "windows" or platform.uname().release.lower() == "microsoft":
        caminho_inicio = os.environ["USERPROFILE"]
        caminho_config = f"{caminho_inicio}/Músicas/Configurações/"
        caminho_cache = f"{caminho_inicio}/Músicas/Cache/spotifyAPItoken"

    elif platform.system().lower() == "linux":
        caminho_inicio = os.environ["HOME"]
        caminho_config = f"{caminho_inicio}/.config/spotify-downloader/"
        caminho_cache = f"{caminho_inicio}/.cache/spotifyAPItoken"


def criar_config_api(client_id, client_secret):
    config_api = {
        "client_id": client_id,
        "client_secret": client_secret
    }

    config_arquivo = open(caminho_config + "api.json", "w")
    config_arquivo.write(json.dumps(config_api, indent=4))
    config_arquivo.close()

    print(f"Configuração criada em: {caminho_config}api.json")
    sys.exit(0)


def criar_config(os, navegador, imagens):
    if not os.path.isdir(caminho_config):
        os.makedirs(caminho_config)

    config_principal = {
        "navegador": navegador,
        "imagens": imagens
    }

    config_arquivo = open(caminho_config + "config.json", "w")
    config_arquivo.write(json.dumps(config_principal, indent=4))
    config_arquivo.close()

    print(f"Configuração criada em: {caminho_config}config.json")
    sys.exit(0)


def abrir_config():
    global sp
    global config

    # Abre o arquivo de configuração da API
    while True:
        if os.path.isfile(caminho_config + "api.json"):
            config_api = json.load(open(caminho_config + "api.json"))
            break
        else:
            print("A configuração da API não foi criada")
            sys.exit(0)

    # Conecta com a API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config_api["client_id"],
                                                   client_secret=config_api["client_secret"],
                                                   redirect_uri="http://127.0.0.1:3000",
                                                   scope="playlist-read-private",
                                                   cache_path=caminho_cache))
    
    # Abre o arquivo de configuração
    while True:
        if os.path.isfile(caminho_config + "config.json"):
            config = json.load(open(caminho_config + "config.json"))
            arquivos = list()

            # Pega o nome dos arquivos importados na config
            try:
                for nome_arquivo in config["importar"]["arquivo"]:
                    arquivos.append(nome_arquivo)
            except:
                pass

            # Pega o nome dos diretórios importados na config
            try:
                for i in range(len(config["importar"]["diretorio"])):
                    for nome_arquivo_em_dir in os.listdir(caminho_config + config["importar"]["diretorio"][i]):
                        arquivos.append(f"{config['importar']['diretorio'][i]}/{nome_arquivo_em_dir}")
            except:
                pass

            # Adiciona os arquivos importados para o dicionário "config"
            if len(arquivos) != 0:
                # Adiciona "musica" e "album" à config se não existirem
                if not "musica" in config:
                    config["musica"] = []
                if not "album" in config:
                    config["album"] = []

                for nome_arquivo in arquivos:
                    modulo_config = json.load(open(caminho_config + nome_arquivo))
                    try:
                        for musica in modulo_config["musica"]:
                            config["musica"].append(musica)
                    except:
                        pass
    
                    try:
                        for album in modulo_config["album"]:
                            config["album"].append(album)
                    except:
                        pass

            break
        else:
            print("A configuração não foi criada")
            sys.exit(0)


def criar_pastas():
    if not os.path.isdir(f"{caminho_inicio}/Músicas/Artistas"):
        os.makedirs(f"{caminho_inicio}/Músicas/Artistas")
    if not os.path.isdir(f"{caminho_inicio}/Músicas/Playlists"):
        os.makedirs(f"{caminho_inicio}/Músicas/Playlists")


def pegar_album(album_url):
    album = sp.album(album_id=album_url)
    album_faixas = sp.album_tracks(album_id=album_url)

    # Itera sobre as músicas do álbum
    for musica in album_faixas['items']:
        musica['album'] = {
            "name": album['name'],
            "release_date": album['release_date'],
            "images": [{"url": album['images'][0]['url']}]
        }
        baixar_musicas(musica)


def pegar_playlists():
    playlists_todas = sp.current_user_playlists()
    playlist_id = list()

    # Pega o id de cada playlist
    for id in playlists_todas['items']:
        playlist_id.append(id['id'])

    for i in range(playlists_todas['total']):
        # Abre o arquivo da playlist
        playlist_arquivo = open(f"{caminho_inicio}/Músicas/Playlists/{playlists_todas['items'][i]['name']}.m3u", "w")

        # Retorna todas as músicas da playlist em uma lista
        playlist = sp.playlist_tracks(playlist_id[i])
        faixas = playlist['items']
        while playlist['next']:
            playlist = sp.next(playlist)
            faixas.extend(playlist['items'])

        # Itera sobre as músicas da playlist
        for playlist_itens in faixas:
            musica = playlist_itens['track']
            caminho_arquivo = baixar_musicas(musica, None, True)

            # Escreve no arquivo da playlist
            playlist_arquivo.write(f"{caminho_arquivo}.mp3\n")

        playlist_arquivo.close()


def pegar_musica(musica_info):
    musica = sp.track(track_id=musica_info["url-spotify"])
    url = None

    # Permite que não seja necessário escolher um link do youtube
    try:
        url = musica_info["url-youtube"]
    except:
        pass

    baixar_musicas(musica, url)


def baixar_musicas(musica, url_youtube = None, playlist = False):
    nome_artista = musica['artists'][0]['name']
    nome_album = musica['album']['name']
    nome_musica = musica['name']

    # Limpa o nome das pastas e arquivos
    nome_artista = limpar_nome(nome_artista)
    nome_album = limpar_nome(nome_album)
    nome_musica = limpar_nome(nome_musica)
    nome_limpo = f"{nome_artista}/{nome_album}/{nome_musica}"

    caminho_arquivo = f"{caminho_inicio}/Músicas/Artistas/{nome_limpo}"

    # Checa se a música já foi instalada. Se não, baixa
    if not os.path.isfile(f"{caminho_arquivo}.mp3"):
        print(f"{musica['name']} - {musica['artists'][0]['name']}")

        # Pega a capa do álbum
        capa_album = None
        if config["imagens"] == True:
            capa_album = requests.get(musica['album']['images'][0]['url']).content

        baixar_mp3(musica, caminho_arquivo, capa_album, url_youtube)

    # Se for uma playlist, retorna o caminho do arquivo para criar a playlist
    if playlist == True:
        return caminho_arquivo


def limpar_nome(nome):
    nome = nome.lower()
    nome = nome.replace(" ", "_")
    nome = nome.replace("/", "")
    nome = nome.replace("(", "").replace(")", "")
    nome = nome.replace("-", "")
    nome = nome.replace(":", "")
    nome = nome.replace("'", "")

    return nome


def baixar_mp3(musica, caminho_arquivo, capa_album, url_youtube):
    # Opções de download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
            }],
        'outtmpl': f'{caminho_arquivo}.%(ext)s',
        'quiet': 'true'
    }

    if config["navegador"] != None:
        ydl_opts['cookiesfrombrowser'] = (config["navegador"],)

    # Query de busca
    query = f"ytsearch: {musica['name']} {musica['artists'][0]['name']}"

    # Checa se um URL foi definido
    if url_youtube != None:
        query = url_youtube

    # Download do mp3
    while True:
        try:
            print("     Baixando")
            yt_dlp.YoutubeDL(ydl_opts).download([query])
        # Faz com que seja possível forçar a interrupção do programa
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("     Erro ao baixar a música, tentando novamente")
        else:
            break

    # Adiciona metadados ao arquivo
    while True:
        try:
            audio = ID3(f"{caminho_arquivo}.mp3")
            audio.add(TIT2(encoding = 3, text = musica['name']))
            audio.add(TPE1(encoding = 3, text = musica['artists'][0]['name']))
            audio.add(TALB(encoding = 3, text = musica['album']['name']))
            audio.add(TDRC(encoding = 3, text = musica['album']['release_date']))
            audio.add(TRCK(encoding = 3, text = str(musica['track_number'])))
            audio.save()
            if not capa_album == None:
                audio.add(APIC(encoding = 3, mime = 'image/jpeg', type = 3, data = capa_album))
        # Faz com que seja possível forçar a interrupção do programa
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("     Erro na adição dos metadados, tentando novamente")
        else:
            break
