# test-api
Atividade da Pós-graduação na UniFAP, testes em uma API.

## Requisitos

- [Python ^3.7](https://www.python.org/downloads/)

## Instruções

### Instalar Dependências

_(Opcional)_ Crie um ambiente virtual para instalar as dependências separadamente do seus outros projetos em Python:

  ```bash
  # Windows:
  python -m venv env
  .\env\Scripts\activate

  # Unix:
  python3 -m venv env
  source env/bin/activate
  ```

Agora, realize a instalação das dependências:

  ```bash
  pip install -r requirements.txt
  ```

### Executar Projeto

Execute na raiz do projeto:
  
  ```bash
  flask --app app run
  # ou
  python -m flask --app app run
  ```

Pronto! A API estará disponível em [localhost:5000](localhost:5000)

## Rotas

1. GET - localhost:5000/estatistica
2. POST - localhost:5000/transacao
3. DELETE - localhost:5000/transacao
4. GET - localhost:5000/transacao/{id}
5. DELETE - localhost:5000/transacao/{id}