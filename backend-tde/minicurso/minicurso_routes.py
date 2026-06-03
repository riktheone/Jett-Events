
from minicurso.minicurso_controller import MinicursoBC
from flask import Blueprint, request
from minicurso.minicurso import Minicurso

minicursoRoutes = Blueprint("minicurso", __name__)
minicursoBC = MinicursoBC()


@minicursoRoutes.route("/api/v1/inscricao/minicurso/<int:idMinicurso>")
def obterInscritosEmMinicurso(idMinicurso):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterInscritosEmMinicurso(request.headers["Authorization"], idMinicurso)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500


@minicursoRoutes.route("/api/v1/minicurso")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterTodos(request.headers["Authorization"])
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/minicurso/<int:id>")
def obterPorId(id):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.obterPorId(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/inscricao/minicurso", methods=['POST'])
def inscrever():
    try:
        if "Authorization" in request.headers:
            if request.json and "id_minicurso" in request.json and "id_usuario_participante" in request.json:
                return minicursoBC.inscrever(request.headers["Authorization"], request.json["id_minicurso"], request.json["id_usuario_participante"])
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/inscricao/minicurso/<int:idMinicurso>/<int:idParticipante>", methods=['DELETE'])
def removerInscricao(idMinicurso, idParticipante):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.removerInscricao(request.headers["Authorization"], idMinicurso, idParticipante)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/minicurso", methods=['POST'])
def salvar():
    try:
        if "Authorization" in request.headers:
            if request.json and "id_evento" in request.json and "nome" in request.json and "descricao" in request.json and "dt_minicurso" in request.json and "horario_inicio_minicurso" in request.json and "horario_fim_minicurso" in request.json and "nome_instrutor" in request.json and "minicurriculo_instrutor" in request.json and "dt_limite_inscricao" in request.json and "numero_vagas" in request.json:
                minicurso = Minicurso(0, **request.json)
                return minicursoBC.salvar(request.headers["Authorization"], minicurso)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/minicurso/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" in request.headers:
            if request.json and "id_evento" in request.json and "nome" in request.json and "descricao" in request.json and "dt_minicurso" in request.json and "horario_inicio_minicurso" in request.json and "horario_fim_minicurso" in request.json and "nome_instrutor" in request.json and "minicurriculo_instrutor" in request.json and "dt_limite_inscricao" in request.json and "numero_vagas" in request.json:
                minicurso = Minicurso(id, **request.json)
                return minicursoBC.atualizar(request.headers["Authorization"], minicurso)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@minicursoRoutes.route("/api/v1/minicurso/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            return minicursoBC.remover(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500