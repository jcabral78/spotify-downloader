import os
import requests
import arquivos

def baixar_musica(sp, config, caminho_arquivo_inicio, musica_info):
    musica = sp.track(track_id=musica_info["url-spotify"])
    caminho_arquivo = f"{caminho_arquivo_inicio}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

    # Checa se a música já foi instalada, se não, baixa
    if not os.path.isfile(f"{caminho_arquivo}.mp3"):
        print(f"Baixando: {musica['name']} - {musica['artists'][0]['name']}")
        capa_album = None
        if config["imagens"] == True:
            capa_album = requests.get(musica['album']['images'][0]['url']).content
        arquivos.baixar_mp3(musica, caminho_arquivo, capa_album, musica_info["url-youtube"])
