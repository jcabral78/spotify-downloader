# spotify-downloader

Um aplicativo que automatiza a instalação e organização de playlists locais usando o spotify. Atualmente só possui suporte para Linux.

## Features

- Baixar playlists.
- Baixar álbuns.

OBS: Todas as músicas são instaladas com os metadados importantes (título, artista, etc) já inseridos.

## Configuração

A configuração é feita por um arquivo json.

### Opções

- navegador: Escreva o nome do seu navegador (chrome, firefox, etc) para a coleta de cookies.
- imagens: Usado para determinar se capas de álbuns vão ou não ser instaladas.
- musica: Usado para instalar músicas separadas e selecionar qual vídeo do youtube deve ser usado.
- album: Usado para instalar álbuns automaticamente.

### Exemplo de Configuração

    {
        "navegador": "firefox",
        "imagens": false,
    
        "musica": [
            {
                "nome": "Bulls on Parade",
                "url-spotify": "https://open.spotify.com/intl-pt/track/0tZ3mElWcr74OOhKEiNz1x?si=cc34f903bd84470a",
                "url-youtube": "https://youtu.be/DvdeE6KzrTc?si=BXmVAlEFx7ti1Bq1"
            }
        ],

        "album": [
            {
                "nome": "Toxicity",
                "url": "https://open.spotify.com/intl-pt/album/6jWde94ln40epKIQCd8XUh"
            }
        ]
    }

## Instalação

### Dependências

- python3
- pip
- make
***

Após instalar as dependências, vá para o terminal e siga estes passos para a instalação:

    # Clonar o repositório
    git clone https://github.com/jcabral78/spotify-downloader.git

    # Entrar no diretório do projeto
    cd spotify-downloader

    # Instalar o projeto (talvez seja necessário rodar com sudo)
    make install

Para mais informações nos comandos disponíveis com make, use `make help`.

### Setup da API

Vá para https://developer.spotify.com e crie um aplicativo no Dashboard. Após criá-lo, adicione "http://127.0.0.1:3000" no Redirect URI. O projeto vai demandar o Client ID e o Client Secret.
