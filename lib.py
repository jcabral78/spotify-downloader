import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TRCK, APIC
import os
import json
import requests

def criar_pastas():
    if not os.path.isdir(f"{os.environ['HOME']}/Músicas/Artistas"):
        os.makedirs(f"{os.environ['HOME']}/Músicas/Artistas")
    if not os.path.isdir(f"{os.environ['HOME']}/Músicas/Playlists"):
        os.makedirs(f"{os.environ['HOME']}/Músicas/Playlists")

def abrir_config():
    global config
    global config_api
    global sp

    caminho_config = f"{os.environ['HOME']}/.config/spotify-downloader/config.json"
    caminho_config_api = f"{os.environ['HOME']}/.config/spotify-downloader/api.json"
    
    # Abre o arquivo de configuração
    try:
        config = json.load(open(caminho_config))
    except:
        criar_config(caminho_config)
    
    # Abre o arquivo de configuração da API
    try:
        config_api = json.load(open(caminho_config_api))
    except:
        criar_config_api(caminho_config_api)

    try:
        # Setup da API
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config_api["client_id"],
                                                       client_secret=config_api["client_secret"],
                                                       redirect_uri="http://127.0.0.1:3000",
                                                       scope="playlist-read-private",
                                                       cache_path=f"{os.environ['HOME']}/.cache/spotifyAPItoken"))
    except:
        print("Erro ao conectar com a API do Spotify")
        exit(0)

def criar_config(caminho_config):
    if not os.path.isdir(caminho_config):
        os.makedirs(caminho_config)

    config_padrao = {
        "imagens": False
    }

    config_arquivo = open(caminho_config, "w")
    config_arquivo.write(json.dumps(config_padrao, indent=4))
    config_arquivo.close()

    print(f"Configuração criada em: {caminho_config}")
    exit(0)

def criar_config_api(caminho_config_api):
    client_id = input("Escreva o client id: ")
    client_secret = input("Escreva o client secret: ")

    config_api = {
        "client_id": client_id,
        "client_secret": client_secret
    }

    config_arquivo = open(caminho_config_api, "w")
    config_arquivo.write(json.dumps(config_api, indent=4))
    config_arquivo.close()

    print(f"Configuração criada em: {caminho_config_api}")
    exit(0)

def baixar_album(album_url):
    album = sp.album(album_id=album_url)
    album_faixas = sp.album_tracks(album_id=album_url)

    # Imprime as músicas da playlist e baixa
    for musica in album_faixas['items']:
        musica['album'] = {
            "name": album['name'],
            "release_date": album['release_date']
        }
        caminho_arquivo = f"{os.environ['HOME']}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

        # Checa se a música já foi instalada, se não, baixa
        if not os.path.isfile(f"{caminho_arquivo}.mp3"):
            print(f"{musica['name']} - {musica['artists'][0]['name']}")
            capa_album = None
            if config["imagens"] == True:
                capa_album = requests.get(album['images'][0]['url']).content
            baixar_mp3(musica, caminho_arquivo, capa_album)


def baixar_playlists():
    playlists_all = sp.current_user_playlists()
    playlist_id = list()
    i = 0

    # Pega o id de cada playlist
    for id in playlists_all['items']:
        playlist_id.append(id['id'])

    while playlists_all['total'] > i:
        # Abre o arquivo da playlist
        playlist_arquivo = open(f"{os.environ['HOME']}/Músicas/Playlists/{playlists_all['items'][i]['name']}.m3u", "w")

        # Retorna todas as músicas da playlist em uma lista
        playlist = sp.playlist_tracks(playlist_id[i])
        faixas = playlist['items']
        while playlist['next']:
            playlist = sp.next(playlist)
            faixas.extend(playlist['items'])

        # Imprime as músicas da playlist e baixa
        for playlist_itens in faixas:
            musica = playlist_itens['track']
            caminho_arquivo = f"{os.environ['HOME']}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

            # Checa se a música já foi instalada, se não, baixa
            if not os.path.isfile(f"{caminho_arquivo}.mp3"):
                print(f"{musica['name']} - {musica['artists'][0]['name']}")
                capa_album = None
                if config["imagens"] == True:
                    capa_album = requests.get(musica['album']['images'][0]['url']).content
                baixar_mp3(musica, caminho_arquivo, capa_album)

            # Escreve no arquivo da playlist
            playlist_arquivo.write(f"{caminho_arquivo}.mp3\n")

        i += 1
        playlist_arquivo.close()

def baixar_musica(musica_info):
    musica = sp.track(track_id=musica_info["url-spotify"])
    caminho_arquivo = f"{os.environ['HOME']}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

    # Checa se a música já foi instalada, se não, baixa
    if not os.path.isfile(f"{caminho_arquivo}.mp3"):
        print(f"{musica['name']} - {musica['artists'][0]['name']}")
        capa_album = None
        if config["imagens"] == True:
            capa_album = requests.get(musica['album']['images'][0]['url']).content
        baixar_mp3(musica, caminho_arquivo, capa_album, musica_info["url-youtube"])

def baixar_mp3(musica, caminho_arquivo, capa_album, url_youtube = None):
    # Opções para download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
            }],
        'cookiefile': f'{os.environ["HOME"]}/.cache/cookies.txt',
        'outtmpl': f'{caminho_arquivo}.%(ext)s',
        'quiet': 'true'
    }

    # Query de busca
    query = f"ytsearch: {musica['name']} {musica['artists'][0]['name']}"

    if url_youtube != None:
        query = url_youtube

    # Download do mp3
    while True:
        try:
            print("     Baixando")
            yt_dlp.YoutubeDL(ydl_opts).download([query])
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
        except:
            print("     Erro na adição dos metadados, tentando novamente")
        else:
            break
