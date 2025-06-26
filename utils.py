import json

import jsonschema
from flask import Response
from jsonschema import validate


def validar_campos(data:dict) -> bool:  
  schema_transacao = {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "valor": {"type": "number"},
      "dataHora": {"type": "string"}
    }
  }

  try:
    validate(instance=data, schema=schema_transacao)
  except jsonschema.exceptions.ValidationError:
    return False
  return True

 
def gerar_resposta(status:int, mensagem:str, conteudo={}) -> Response:
  corpo = {}
  corpo["mensagem"] = mensagem
  corpo["conteudo"] = conteudo
  return Response(json.dumps(corpo), status=status, mimetype="application/json")
