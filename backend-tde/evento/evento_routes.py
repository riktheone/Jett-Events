from flask import Blueprint, request

from evento.evento import Evento
from evento.evento_controller import EventoBC

eventoRoutes = Blueprint("evento", __name__)
eventoBC = EventoBC()


@eventoRoutes.route("/api/v1/evento/programacao/<int:idEvento>")
def obterProgramacao(idEvento):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterProgramacao(request.headers["Authorization"], idEvento)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento/periodo")
def obterTodosPorPeriodo():
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        dt_inicio = request.args.get("dt_inicio")
        dt_fim = request.args.get("dt_fim")
        body = request.get_json(silent=True) or {}
        if body:
            dt_inicio = body.get("dt_inicio", dt_inicio)
            dt_fim = body.get("dt_fim", dt_fim)
        if dt_inicio and dt_fim:
            return eventoBC.obterTodosPorPeriodo(request.headers["Authorization"], dt_inicio, dt_fim)
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/inscricao/evento/<int:idEvento>")
def obterInscritosEmEvento(idEvento):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterInscritosEmEvento(request.headers["Authorization"], idEvento)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterTodos(request.headers["Authorization"])
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento/<int:id>")
def obterPorId(id):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterPorId(request.headers["Authorization"], id)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/inscricao/evento", methods=['POST'])
def inscrever():
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["id_evento", "cpf_participante", "nome_participante", "email_participante", "telefone_participante"]
        if request.json and all(campo in request.json for campo in campos):
            return eventoBC.inscrever(request.headers["Authorization"], request.json["id_evento"], request.json)
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/inscricao/evento/<int:idEvento>/<int:idParticipante>", methods=['DELETE'])
def removerInscricao(idEvento, idParticipante):
    try:
        if "Authorization" in request.headers:
            return eventoBC.removerInscricao(request.headers["Authorization"], idEvento, idParticipante)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento", methods=['POST'])
def salvar():
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["nome", "dt_inicio", "dt_fim", "descricao", "nome_responsavel", "cpf_responsavel", "email_responsavel", "numero_vagas", "dt_limite_inscricao"]
        if request.json and all(campo in request.json for campo in campos):
            return eventoBC.salvar(request.headers["Authorization"], Evento(0, **request.json))
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["nome", "dt_inicio", "dt_fim", "descricao", "nome_responsavel", "cpf_responsavel", "email_responsavel", "numero_vagas", "dt_limite_inscricao"]
        if request.json and all(campo in request.json for campo in campos):
            return eventoBC.atualizar(request.headers["Authorization"], Evento(id, **request.json))
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@eventoRoutes.route("/api/v1/evento/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            return eventoBC.remover(request.headers["Authorization"], id)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500
