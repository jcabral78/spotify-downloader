# Feito para ser rodado com "make"
make: setup build

setup:
	@echo "Criando o ambiente virtual"
	@python -m venv venv
	@echo "Instalando as dependências"
	@./venv/bin/pip install -r requirements.txt

build:
	@echo "Instalando as dependências"
	@./venv/bin/pip install pyinstaller
	@echo "Construindo o binário"
	@./venv/bin/pyinstaller --onefile --name spotify-downloader main.py

install:
	@echo "Instalando o projeto"
	@cp -f ./dist/spotify-downloader /usr/local/bin/

clean:
	@echo "Limpando o projeto"
	@rm -rf __pycache__
	@rm -rf venv
	@rm -rf build
	@rm -rf dist
	@rm -rf main.spec
	@rm -rf spotify-downloader.spec

help:
	@echo "make setup:"
	@echo "	Cria o ambiente virtual e instala as dependências"
	@echo "make build:"
	@echo "	Instala as dependências de build e cria um binário do projeto"
	@echo "make install:"
	@echo "	Copia o binário para /usr/local/bin (talvez tenha que ser executado com sudo)"
	@echo "make clean:"
	@echo "	Limpa a pasta do projeto"
