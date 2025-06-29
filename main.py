import os
import json
import lib

lib.abrir_config()
lib.criar_pastas()

print("O que você quer baixar?")
print("1) Álbum")
print("2) Outros")
opcao = int(input())

match opcao:
    case 1:
        url = input("Escreva o URL de um álbum: ")
        lib.pegar_album(url)

    case 2:
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
                url = album_config["url"]
                lib.pegar_album(url)
        except:
            pass

    case _:
        print("Erro de input")
