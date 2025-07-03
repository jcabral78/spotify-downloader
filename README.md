# spotify-downloader

Uma ferramenta CLI que automatiza a instalação e organização de playlists locais usando o spotify. Atualmente só possui suporte para Linux.

## Features

- Baixar playlists.
- Baixar álbuns.

OBS: Todas as músicas são instaladas com os metadados importantes (título, artista, etc) já inseridos.

## Utilização

A ferramenta pode rodar em quatro opções diferentes: *config*, *config_api*, *álbum* e *normal*.

### Config '-c'

Cria a configuração.

    # Não define nenhum navegador e não instala imagens
    spotify-downloader -c nenhum nao

    # Define o navegador como "firefox" e instala imagens
    spotify-downloader -c firefox sim

Para mais informações, leia [Configuração](#configuração).

### Config-API '-C'

Cria a configuração da API.

    # Define client_id e client_secret
    spotify-downloader -C *client_id* *client_secret*

Para mais informações, leia [Setup da API](#setup-da-api).

### Álbum '-a'

Instala um álbum.

    # Instala o álbum "Dopethrone"
    spotify-downloader -a https://open.spotify.com/intl-pt/album/2ntG8GB5e2RuOYkSmBo1ij?si=k-m2WqJkTrqCyGWXLH8-tw

### Normal

O modo normal da ferramenta. Instala músicas separadas, álbuns definidos na configuração e playlists.

    # Para usar a ferramenta no modo normal, basta usá-la sem nenhuma flag
    spotify-downloader

## Configuração

A configuração é feita por um arquivo json.

### Opções

- navegador: Escreva o nome do seu navegador (chrome, firefox, etc) para instalar conteúdo com restrição de idade, ou "null" se não quiser fazer a coleta de cookies.
- imagens: Usado para determinar se capas de álbuns vão ou não ser instaladas (true ou false).
- musica: Usado para instalar músicas separadas.
    - url-spotify: Link da música no spotify.
    - url-youtube: Link do vídeo que será usado para o download no youtube (opcional).
- album: Usado para instalar álbuns automaticamente.
    - url: Link do álbum no spotify.
- importar: Usado para importar arquivos e diretórios
    - arquivo: Importa arquivos separados.
    - diretorio: Importa todos os arquivos em um diretório.

### Exemplo de Configuração

    {
        "navegador": null,
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
        ],

        "importar": {
            "arquivo": [
                "audioslave.json"
            ],
    
            "diretorio": [
                "artistas"
            ]
        }
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

    # Instalar o projeto (talvez seja necessário rodar "make install" com sudo)
    make
    make install

Para mais informações nos comandos disponíveis com make, use `make help`.

### Setup da API

Vá para https://developer.spotify.com e crie um aplicativo no Dashboard. Após criá-lo, adicione "http://127.0.0.1:3000" no Redirect URI. Será necessário definir o Client ID e o Client Secret usando a flag '-C', para mais informações em como usá-la, leia [Utilização](#utilização).
