import pytz
from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from utils import validar_campos, gerar_resposta


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
TIMEZONE = pytz.timezone("America/Sao_Paulo")


db = SQLAlchemy(app)
with app.app_context():
  class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(36), unique = True, nullable = False)
    valor = db.Column(db.Float, nullable = False)
    dataHora = db.Column(db.DateTime(timezone = True))

    def get_json(self):
      return {"uuid": self.uuid, "valor": self.valor, "dataHora": str(self.dataHora)}
    
  db.drop_all()
  db.create_all()


  # Receber Transação: POST /transacao
  @app.route("/transacao", methods=["POST"])
  def salvar():
    corpo = request.get_json()

    if "id" not in corpo or "valor" not in corpo or "dataHora" not in corpo:
      return gerar_resposta(400, "Requisição inválida")

    if validar_campos(corpo) is False:
      return gerar_resposta(400, "Transação inválida")
    
    if corpo["valor"] < 0:
      return gerar_resposta(422, "Valor inválido na transação")
    
    tempoAtual = datetime.now(TIMEZONE)
    dataHora = datetime.fromisoformat(corpo["dataHora"])
    
    if dataHora > tempoAtual:
      return gerar_resposta(422, "Horário inválido na transação")

    try:
      db.one_or_404(db.select(Transacao).filter_by(uuid=corpo["id"]))
      return gerar_resposta(422, "Transação já cadastrada")
    except:
      transacao = Transacao(
        uuid = corpo["id"], 
        valor = corpo["valor"],
        dataHora = dataHora
      )

      try:
        db.session.add(transacao)
        db.session.commit()
        return gerar_resposta(201, "Registrada com sucesso")
      except Exception as e:
        print("Erro: ", e)
        return gerar_resposta(400, "Erro no cadastro")


  # Recuperar uma transação: GET /transacao/{id}
  @app.route("/transacao/<uuid>", methods=["GET"])
  def buscar_por_uuid(uuid):
    try:
      stmt = db.select(Transacao).filter_by(uuid=uuid)
      transacao = db.session.execute(stmt).scalar_one()
      return gerar_resposta(200, "Transação encontrada", transacao.get_json())
    except Exception as e:
      print("Erro: ", e)
      return gerar_resposta(404, "Nenhuma transação encontrada")


  # Limpar Transação: DELETE /transacao/{id}
  @app.route("/transacao/<uuid>", methods=["DELETE"])
  def deletar_por_uuid(uuid):
    try:
      stmt = db.select(Transacao).filter_by(uuid=uuid)
      transacao = db.session.execute(stmt).scalar_one()
    except Exception as e:
      print("Erro: ", e)
      return gerar_resposta(404, "Transação não encontrada")

    try:
      db.session.delete(transacao)
      db.session.commit()
      return gerar_resposta(200, "Deletada com sucesso")
    except Exception as e:
      print("Erro: ", e)
      return gerar_resposta(400, "Erro na exclusão")


  # Limpar Transações: DELETE /transacao
  @app.route("/transacao", methods=["DELETE"])
  def deletar_todas():
    stmt = db.select(Transacao).order_by(Transacao.dataHora)
    transacoes = db.session.execute(stmt).scalars()

    for t in transacoes:
      try:
        db.session.delete(t)
        db.session.commit()
      except Exception as e:
        print("Erro: ", e)
        return gerar_resposta(400, "Erro na exclusão")
    return gerar_resposta(200, "Deletadas com sucesso")


  # Calcular Estatísticas: GET /estatistica
  @app.route("/estatistica", methods=["GET"])
  def calcular_dados():
    stmt = db.select(Transacao).order_by(Transacao.dataHora)
    transacoes = db.session.execute(stmt).scalars()

    valores = []
    for t in transacoes:
      transacao = t.get_json()
      valores.append(transacao["valor"])

    dados = {}
    dados["count"] = len(valores)
    dados["sum"] = sum(valores, start=0)
    dados["avg"] = sum(valores, start=0) / len(valores) if len(valores) else 0
    dados["min"] = min(valores, default=0)
    dados["max"] = max(valores, default=0)

    return gerar_resposta(200, "Estatísticas calculadas!", dados)


  if __name__ == "__main__":
    app.run(debug = True)