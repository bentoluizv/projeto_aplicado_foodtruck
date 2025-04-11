# Projeto Aplicado SENAI 2025

O Projeto Aplicado é desenvolvido pelos alunos da quarta fase do curso de Análise e Desenvolvimento de Sistemas do SENAI SC em Florianópolis. Trata-se de uma aplicação web escrita em Python, utilizando o framework FastAPI para o backend e HTMX para a interação dinâmica no frontend. O objetivo do projeto é integrar os conhecimentos adquiridos ao longo do curso, promovendo a aplicação prática de conceitos como desenvolvimento de APIs, gerenciamento de dependências, versionamento de código e implantação de aplicações em ambientes de produção.

## Requisitos

- Python 3.13

## Ambiente de Desenvolvimento

> **TL:DR**
>
> Linux > Windows

### Instale o Python e o Poetry

1. Instale o Python 3.13 usando o [pyenv](https://github.com/pyenv/pyenv) (Linux) ou [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows):

    ***Linux***

    - Baixe o Pyenv

    ```sh
    curl -fsSL https://pyenv.run | bash
    ```

    - Adicione o Pyenv ao PATH

    ```sh
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
    exec "$SHELL"
    ```

    - Instale o Python

    ```sh
    pyenv install 3.13.0
    ```

    ***Windows***

    ```powershell
    Invoke-WebRequest -UseBasicParsing https://pyenv-win.github.io/pyenv-win/install.ps1 | Invoke-Expression
    pyenv install 3.13.0
    ```

2. Instale o [pipx](https://pypa.github.io/pipx/):

    ***Linux***

    ```sh
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
    ```

    ***Windows***
    - Instale o Scoop

    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri <https://get.scoop.sh> | Invoke-Expression
    ```

    - Instale o Pipx com o Scoop

    ```powershell
    scoop install pipx
    pipx ensurepath
    ```

3. Instale o [Poetry](https://python-poetry.org/docs/#installation) usando o pipx e o Poetry Shell:

    ```sh
    pipx install poetry
    poetry self add poetry-plugin-shell
    ```

### Download do Projeto e Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git projeto_aplicado
    cd projeto_aplicado
    ```

2. Crie um ambiente virtual e instale as dependências:

    ```sh
    poetry env use 3.13 # Crie um ambiente virtual com a versão 3.13
    poetry shell # Ativa o venv
    poetry install # Instala as dependências
    ```

3. Execute a aplicação:

    ```sh
    task dev
    ```

4. Crie um arquivo requirements.txt a partir do Poetry:

    ```sh
    task export
    ```

### Instalação do Docker

1. Instale o Docker seguindo as instruções oficiais para o seu sistema operacional:
    - [Docker para Linux](https://docs.docker.com/engine/install/)
    - [Docker para Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Docker para macOS](https://docs.docker.com/desktop/install/mac-install/)
2. Após a instalação, verifique se o Docker está funcionando corretamente:

    ```sh
    docker --version
    ```

3. Instale o Docker Compose, caso ele não venha incluído na instalação do Docker:
    - [Instruções para instalar o Docker Compose](https://docs.docker.com/compose/install/)
4. Verifique a instalação do Docker Compose:

    ```sh
    docker-compose --version
    ```

5. Certifique-se de que o serviço do Docker está em execução antes de usar os comandos do Docker Compose.

### Uso do Docker Compose

1. Construa e inicie os containers:

    ```sh
    docker-compose up --build
    ```
