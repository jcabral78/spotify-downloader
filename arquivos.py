import yt_dlp
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TRCK, APIC
import os
import json

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


def criar_config(caminho_config_home):
    OS_str = ["linux"]

    print("Escolha o seu sistema")
    print("1) Linux")
    OS = int(input())
    OS = OS - 1

    caminho_config = caminho_config_home[OS]
    os.makedirs(f"{caminho_config}")

    config_padrao = {
        "OS": OS_str[OS],
        "imagens": False
    }

    caminho_config = caminho_config + "/config.json"
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

    caminho_config_api = caminho_config_api + "/api.json"
    config_arquivo = open(caminho_config_api, "w")
    config_arquivo.write(json.dumps(config_api, indent=4))
    config_arquivo.close()

    print(f"Configuração criada em: {caminho_config_api}")
    exit(0)
    
def criar_pastas(caminho_arquivo_inicio):
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Artistas"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Artistas")
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Playlists"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Playlists")
