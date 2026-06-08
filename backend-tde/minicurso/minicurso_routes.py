from flask import Blueprint, request

from minicurso.minicurso import Minicurso
from minicurso.minicurso_controller import MinicursoBC

minicursoRoutes = Blueprint("minicurso", __name__)
minicursoBC = MinicursoBC()


@minicursoRoutes.route("/api/v1/inscricao/minicurso/<int:idMinicurso>")
def obterInscritosEmMinicurso(idMinicurso):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterInscritosEmMinicurso(request.headers["Authorization"], idMinicurso)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/minicurso")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterTodos(request.headers["Authorization"])
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/minicurso/<int:id>")
def obterPorId(id):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterPorId(request.headers["Authorization"], id)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/inscricao/minicurso", methods=['POST'])
def inscrever():
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["id_minicurso", "cpf_participante", "nome_participante", "email_participante", "telefone_participante"]
        if request.json and all(campo in request.json for campo in campos):
            return minicursoBC.inscrever(request.headers["Authorization"], request.json["id_minicurso"], request.json)
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/inscricao/minicurso/<int:idMinicurso>/<int:idParticipante>", methods=['DELETE'])
def removerInscricao(idMinicurso, idParticipante):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.removerInscricao(request.headers["Authorization"], idMinicurso, idParticipante)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/minicurso", methods=['POST'])
def salvar():
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["id_evento", "nome", "descricao", "dt_minicurso", "horario_inicio_minicurso", "horario_fim_minicurso", "nome_instrutor", "minicurriculo_instrutor", "dt_limite_inscricao", "numero_vagas"]
        if request.json and all(campo in request.json for campo in campos):
            return minicursoBC.salvar(request.headers["Authorization"], Minicurso(0, **request.json))
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/minicurso/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" not in request.headers:
            return {"msg": "Sem permissao"}, 401
        campos = ["id_evento", "nome", "descricao", "dt_minicurso", "horario_inicio_minicurso", "horario_fim_minicurso", "nome_instrutor", "minicurriculo_instrutor", "dt_limite_inscricao", "numero_vagas"]
        if request.json and all(campo in request.json for campo in campos):
            return minicursoBC.atualizar(request.headers["Authorization"], Minicurso(id, **request.json))
        return {"msg": "Esta faltando parametros"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500


@minicursoRoutes.route("/api/v1/minicurso/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.remover(request.headers["Authorization"], id)
        return {"msg": "Sem permissao"}, 401
    except Exception as error:
        return {"msg": str(error)}, 500
