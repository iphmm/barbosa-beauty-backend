# Studio Barbosa Beauty - Back-end 💅

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16-A30000?style=for-the-badge&logo=django-rest-framework&logoColor=white)

## 📄 Sobre o Projeto

Este repositório contém o código-fonte do back-end para o sistema de agendamento do **Studio Barbosa Beauty**. A aplicação é desenvolvida em Python com o framework Django e serve como uma API RESTful para gerenciar serviços, clientes e agendamentos.

## ✨ Tecnologias Principais

- **Python:** Linguagem de programação principal.
- **Django:** Framework web para o desenvolvimento rápido e seguro.
- **Django REST Framework (DRF):** Toolkit para a construção de APIs Web.
- **Pillow:** Biblioteca para manipulação e processamento de imagens.
- **SQLite3:** Banco de dados padrão para o ambiente de desenvolvimento.

---

## 🚀 Guia de Instalação e Configuração

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

- **Python** (versão 3.10 ou superior)
- **Git**

> **Atenção (Usuários Windows):** Durante a instalação do Python, marque a caixa de seleção **"Add Python to PATH"** para evitar problemas na linha de comando.

### Passos para Instalação

1.  **Clone o Repositório**
    Abra seu terminal e navegue até a pasta onde deseja salvar o projeto.
    ```bash
    # Clone o projeto do GitHub
    git clone <URL_DO_SEU_REPOSITORIO_GIT>

    # Entre na pasta do projeto
    cd barbosa-beauty-backend
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`)**
    Isso cria um ambiente isolado para as dependências do projeto.

    - **No Windows:**
      ```bash
      # Cria o ambiente virtual
      python -m venv venv

      # Ativa o ambiente
      venv\Scripts\activate
      ```

    - **No macOS / Linux:**
      ```bash
      # Cria o ambiente virtual
      python3 -m venv venv

      # Ativa o ambiente
      source venv/bin/activate
      ```
    Após a ativação, você verá `(venv)` no início da linha do seu terminal.

3.  **Instale as Dependências**
    Com o ambiente virtual ativo, instale todas as bibliotecas listadas no arquivo `requirements.txt` com um único comando.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as Migrações do Banco de Dados**
    Este comando cria as tabelas necessárias no banco de dados.
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Superusuário**
    Para acessar o painel de administração do Django, você precisa de um usuário administrador.
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir um nome de usuário, e-mail e senha.

---

## ▶️ Rodando a Aplicação

Com tudo configurado, inicie o servidor de desenvolvimento.

```bash
python manage.py runserver
```

A aplicação estará disponível nos seguintes endereços:

- **API Interativa:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **Painel de Administração:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🌿 Fluxo de Trabalho com Git (Branches)

Para manter a organização e a qualidade do código, seguimos o seguinte fluxo:

1.  **Nunca envie código diretamente para a branch `main`**.
2.  Antes de iniciar uma nova tarefa, atualize sua branch `main` local: `git checkout main && git pull origin main`.
3.  Crie uma nova branch para sua funcionalidade: `git checkout -b <tipo>/<nome-da-funcionalidade>` (ex: `feature/api-agendamentos`).
4.  Faça seus commits na sua branch.
5.  Envie a branch para o repositório remoto: `git push origin <nome-da-sua-branch>`.
6.  Abra um **Pull Request (PR)** no GitHub para que o código seja revisado pela equipe antes de ser integrado à `main`.