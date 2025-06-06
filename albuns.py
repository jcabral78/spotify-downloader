import os
import requests
from arquivos import baixar_mp3, config, caminho_arquivo_inicio
from api import sp

# Retorna todas as músicas de um álbum em uma lista
def pegar_musicas_album(album_id):
    album_faixas = sp.album_tracks(album_id=album_id)
    return album_faixas['items']

def baixar_album(album_url):
    album = sp.album(album_id=album_url)

    # Imprime as músicas da playlist e baixa
    for musica in pegar_musicas_album(album['id']):
        musica['album'] = {
            "name": album['name'],
            "release_date": album['release_date']
        }
        caminho_arquivo = f"{caminho_arquivo_inicio}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

        # Checa se a música já foi instalada, se não, baixa
        if not os.path.isfile(f"{caminho_arquivo}.mp3"):
            print(f"Baixando: {musica['name']} - {musica['artists'][0]['name']}")
            capa_album = None
            if config["imagens"] == True:
                capa_album = requests.get(album['images'][0]['url']).content
            baixar_mp3(musica, caminho_arquivo)
