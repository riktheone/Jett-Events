
from evento.evento_controller import EventoBC
from flask import Blueprint, request
from evento.evento import Evento

eventoRoutes = Blueprint("evento", __name__)
eventoBC = EventoBC()

@eventoRoutes.route("/api/v1/evento/programacao/<int:idEvento>")
def obterProgramacao(idEvento):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterProgramacao(request.headers["Authorization"], idEvento)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento/periodo")
def obterTodosPorPeriodo():
    try:
        if "Authorization" in request.headers:
            if "dt_inicio" in request.json and "dt_fim" in request.json:
                return eventoBC.obterTodosPorPeriodo(request.headers["Authorization"], request.json["dt_inicio"], request.json["dt_fim"])
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/inscricao/evento/<int:idEvento>")
def obterInscritosEmEvento(idEvento):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterInscritosEmEvento(request.headers["Authorization"], idEvento)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterTodos(request.headers["Authorization"])
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento/<int:id>")
def obterPorId(id):
    try:
        if "Authorization" in request.headers:
            return eventoBC.obterPorId(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/inscricao/evento", methods=['POST'])
def inscrever():
    try:
        if "Authorization" in request.headers:
            if request.json and "id_evento" in request.json and "id_usuario_participante" in request.json:
                return eventoBC.inscrever(request.headers["Authorization"], request.json["id_evento"], request.json["id_usuario_participante"])
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/inscricao/evento/<int:idEvento>/<int:idParticipante>", methods=['DELETE'])
def removerInscricao(idEvento, idParticipante):
    try:
        if "Authorization" in request.headers:
            return eventoBC.removerInscricao(request.headers["Authorization"], idEvento, idParticipante)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento", methods=['POST'])
def salvar():
    try:
        if "Authorization" in request.headers:
            if request.json and "nome" in request.json and "dt_inicio" in request.json and "dt_fim" in request.json and "descricao" in request.json and "nome_responsavel" in request.json and "cpf_responsavel" in request.json and "email_responsavel" in request.json and "numero_vagas" in request.json and "dt_limite_inscricao" in request.json:
                evento = Evento(0, **request.json)
                return eventoBC.salvar(request.headers["Authorization"], evento)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" in request.headers:
            if request.json and "nome" in request.json and "dt_inicio" in request.json and "dt_fim" in request.json and "descricao" in request.json and "nome_responsavel" in request.json and "cpf_responsavel" in request.json and "email_responsavel" in request.json and "numero_vagas" in request.json and "dt_limite_inscricao" in request.json:
                evento = Evento(id, **request.json)
                return eventoBC.atualizar(request.headers["Authorization"], evento)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@eventoRoutes.route("/api/v1/evento/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            return eventoBC.remover(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500