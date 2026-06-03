
from palestra.palestra_controller import PalestraBC
from flask import Blueprint, request
from palestra.palestra import Palestra

palestraRoutes = Blueprint("palestra", __name__)
palestraBC = PalestraBC()

@palestraRoutes.route("/api/v1/palestra")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            return palestraBC.obterTodos(request.headers["Authorization"])
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@palestraRoutes.route("/api/v1/palestra/<int:id>")
def obterPorId(id):
    try:
        if "Authorization" in request.headers:
            return palestraBC.obterPorId(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@palestraRoutes.route("/api/v1/palestra", methods=['POST'])
def salvar():
    try:
        if "Authorization" in request.headers:
            if request.json and "id_evento" in request.json and "nome" in request.json and "descricao" in request.json and "dt_palestra" in request.json and "horario_inicio_palestra" in request.json and "horario_fim_palestra" in request.json and "nome_palestrante" in request.json and "minicurriculo_palestrante" in request.json:
                palestra = Palestra(0, **request.json)
                return palestraBC.salvar(request.headers["Authorization"], palestra)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@palestraRoutes.route("/api/v1/palestra/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" in request.headers:
            if request.json and "id_evento" in request.json and "nome" in request.json and "descricao" in request.json and "dt_palestra" in request.json and "horario_inicio_palestra" in request.json and "horario_fim_palestra" in request.json and "nome_palestrante" in request.json and "minicurriculo_palestrante" in request.json:
                palestra = Palestra(id, **request.json)
                return palestraBC.atualizar(request.headers["Authorization"], palestra)
            else:
                return {"msg":"Está faltando parâmetros"}, 422
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@palestraRoutes.route("/api/v1/palestra/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            return palestraBC.remover(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500