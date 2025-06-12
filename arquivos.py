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

def criar_config(caminho_config, caminho_config_todos):
    print("Escolha o seu sistema")
    print("1) Linux")
    OS = int(input())
    OS_str = ["linux"]
    caminho_config = caminho_config_todos[OS - 1]
    os.makedirs(f"{caminho_config}")
    config_arquivo = open(f"{caminho_config}/config.json", "w")
    config_padrao = {
        "OS": OS_str[OS - 1],
        "client_id": "",
        "client_secret": "",
        "imagens": False
    }
    config_arquivo.write(json.dumps(config_padrao, indent=4))
    config_arquivo.close()
    print(f"Configuração criada em: {caminho_config}")
    print("Por favor, mude o que for necessário e tente novamente")
    exit(0)
    
def criar_pastas(caminho_arquivo_inicio):
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Artistas"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Artistas")
    if not os.path.isdir(f"{caminho_arquivo_inicio}/Músicas/Playlists"):
        os.makedirs(f"{caminho_arquivo_inicio}/Músicas/Playlists")
