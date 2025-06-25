import requests
import pytest

uuid = "acde070d-8c4c-4f0d-9d8a-162843c10333"

@pytest.fixture
def base_url():
  return "http://localhost:5000"

# Testes - Receber Transação
def teste_salvar_json_invalido(base_url):
  payload = {
    "id": uuid,
    "v": 123.45,
    "data": "2020-08-07T12:34:56.789-03:00"
  }
  response = requests.post(f"{base_url}/transacao", json=payload)
  assert response.status_code == 400

def teste_salvar_valor_invalido(base_url):
  payload = {
    "id": uuid,
    "valor": -1,
    "dataHora": "2020-08-07T12:34:56.789-03:00"
  }
  response = requests.post(f"{base_url}/transacao", json=payload)
  assert response.status_code == 422

def teste_salvar_data_invalida(base_url):
  payload = {
    "id": uuid,
    "valor": 123.45,
    "dataHora": "2100-01-01T00:00:00.000-03:00"
  }
  response = requests.post(f"{base_url}/transacao", json=payload)
  assert response.status_code == 422

def test_salvar_sucesso(base_url):
  payload = {
    "id": uuid,
    "valor": 123.45,
    # "dataHora": "2020-08-07T12:34:56.789-03:00"
  }
  response = requests.post(f"{base_url}/transacao", json=payload)
  assert response.status_code == 201

def test_salvar_id_invalido(base_url):
  payload = {
    "id": uuid,
    "valor": 123.45,
    "dataHora": "2100-01-01T00:00:00.000-03:00"
  }
  response = requests.post(f"{base_url}/transacao", json=payload)
  assert response.status_code == 422


# Testes - Recuperar uma transação
def test_buscar_por_uuid_erro(base_url):
  response = requests.get(f"{base_url}/transacao/abc123")
  assert response.status_code == 404

def test_buscar_por_uuid_sucesso(base_url):
  response = requests.get(f"{base_url}/transacao/{uuid}")
  assert response.status_code == 200
  assert response.json()["conteudo"]["uuid"] == uuid


# Testes - Limpar Transação
def test_deletar_por_uuid_erro(base_url):
  response = requests.delete(f"{base_url}/transacao/abc123")
  assert response.status_code == 404

def test_deletar_por_uuid_sucesso(base_url):
  response = requests.delete(f"{base_url}/transacao/{uuid}")
  assert response.status_code == 200


# Testes - Limpar Transações
def test_deletar_todas(base_url):
  response = requests.delete(f"{base_url}/transacao")
  assert response.status_code == 200


# Testes - Calcular Estatísticas
def test_calcular_dados(base_url):
  response = requests.get(f"{base_url}/estatistica")
  assert response.status_code == 200


if __name__ == "__main__":
  pytest.main()