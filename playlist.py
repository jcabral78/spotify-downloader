import os
import requests
import json
import arquivos

# Retorna todas as músicas da playlist em uma lista
def pegar_musicas_playlist(sp, id, i):
    playlist = sp.playlist_tracks(id[i])
    faixas = playlist['items']
    while playlist['next']:
        playlist = sp.next(playlist)
        faixas.extend(playlist['items'])
    return faixas


def baixar_playlists(sp, config, caminho_arquivo_inicio):
    playlists_all = sp.current_user_playlists()
    playlist_id = list()
    i = 0
    url_youtube = ""

    # Pega o id de cada playlist
    for id in playlists_all['items']:
        playlist_id.append(id['id'])

    while playlists_all['total'] > i:
        # Abre o arquivo da playlist
        playlist_arquivo = open(f"{caminho_arquivo_inicio}/Músicas/Playlists/{playlists_all['items'][i]['name']}.m3u", "w")

        # Imprime as músicas da playlist e baixa
        for playlist_itens in pegar_musicas_playlist(sp, playlist_id, i):
            musica = playlist_itens['track']
            caminho_arquivo = f"{caminho_arquivo_inicio}/Músicas/Artistas/{musica['artists'][0]['name']}/{musica['album']['name']}/{musica['name']}"

            # Checa se a música já foi instalada, se não, baixa
            if not os.path.isfile(f"{caminho_arquivo}.mp3"):
                print(f"Baixando: {musica['name']} - {musica['artists'][0]['name']}")
                capa_album = None
                if config["imagens"] == True:
                    capa_album = requests.get(musica['album']['images'][0]['url']).content
                arquivos.baixar_mp3(musica, caminho_arquivo, capa_album, url_youtube)

            # Escreve no arquivo da playlist
            playlist_arquivo.write(f"{caminho_arquivo}.mp3\n")

        i += 1
        playlist_arquivo.close()
