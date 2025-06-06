from arquivos import criar_pastas, criar_config
from playlists import *
from albuns import *

criar_pastas()
criar_config()

print("O que você quer baixar?")
print("1) Álbum")
print("2) Playlists")
opcao = int(input())

match opcao:
    case 1:
        url = input("Escreva o URL de um álbum: ")
        baixar_album(url)

    case 2:
        baixar_playlists()

    case _:
        print("Erro de input")
