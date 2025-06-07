import yt_dlp
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TRCK, APIC
import os
import json

try:
    with open(f"{os.environ['HOME']}/.config/spotify-downloader/config.json") as arquivo_config:
        config = json.load(arquivo_config)
except:
    with open(f"/storage/emulated/0/Músicas/Configurações/config.json") as arquivo_config:
        config = json.load(arquivo_config)

match config["OS"]:
    case "linux":
        caminho_arquivo_inicio = f"{os.environ['HOME']}"
    case "android":
        caminho_arquivo_inicio = "/storage/emulated/0"
    case _:
        print("Erro na config: OS")

def criar_pastas():
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Artistas"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Artistas")
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Playlists"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Playlists")

    match config["OS"]:
        case "linux":
            caminho_config = f"{caminho_arquivo_inicio}/.config/spotify-downloader"
            if not os.path.isdir(caminho_config):
                os.makedirs(caminho_config)
        case "android":
            caminho_config = f"{caminho_arquivo_inicio}/Músicas/Configurações"
            if not os.path.isdir(caminho_config):
                os.makedirs(caminho_config)

    return caminho_config

def criar_config(caminho_config):
    if not os.path.isfile(f"{caminho_config}/config.json"):
        config_arquivo = open(f"{caminho_config}/config.json", "w")
        config_padrao = {
            "OS": "",
            "client_id": "",
            "client_secret": "",
            "imagens": False
        }
        config_arquivo.write(json.dumps(config_padrao, indent=4))
        config_arquivo.close()

def baixar_mp3(musica, caminho_arquivo, capa_album):
    # Opções para download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }],
        'outtmpl': f'{caminho_arquivo}.%(ext)s',
        'quiet': 'true'
    }

    # Query de busca
    query = f"ytsearch: {musica['name']} {musica['artists'][0]['name']}"

    # Download do mp3
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

    # Adiciona metadados ao arquivo
    audio = ID3(f"{caminho_arquivo}.mp3")
    audio.add(TIT2(encoding = 3, text = musica['name']))
    audio.add(TPE1(encoding = 3, text = musica['artists'][0]['name']))
    audio.add(TALB(encoding = 3, text = musica['album']['name']))
    audio.add(TDRC(encoding = 3, text = musica['album']['release_date']))
    audio.add(TRCK(encoding = 3, text = str(musica['track_number'])))
    if not capa_album == None:
        audio.add(APIC(encoding = 3, mime = 'image/jpeg', type = 3, data = capa_album))
    audio.save()
