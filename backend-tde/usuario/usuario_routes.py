from usuario.usuario_controller import UsuarioBC
from flask import Blueprint, jsonify, request
from usuario.usuario import Usuario
from util.jwt_util import jwtDecode

usuarioRoutes = Blueprint("usuario", __name__)

@usuarioRoutes.route("/api/v1/usuario/porToken")
def obterUsuarioPorToken():
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            decodedToken = jwtDecode(request.headers["Authorization"])
            if not decodedToken:
                return {"msg":"token inválido"}, 403
            if not "cpf" in decodedToken:
                return {"msg":"token inválido"}, 403
            tuplaUsuario = usuarioBC.obterUsuarioPorCPF(decodedToken["cpf"])
            dictUsuario = {"id":tuplaUsuario[0], "cpf":tuplaUsuario[1], "nome":tuplaUsuario[2], "email":tuplaUsuario[3], "administrador":tuplaUsuario[5]}
            return jsonify(dictUsuario), 200
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario")
def obterTodos():
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            return usuarioBC.obterTodos(request.headers["Authorization"])
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario", methods=['POST'])
def salvar():
    try:
        if 'cpf' in request.json and 'nome' in request.json and 'email' in request.json and 'senha' in request.json:
            if request.json['cpf'] and request.json['nome'] and request.json['email'] and request.json['senha']:
                usuarioBC = UsuarioBC()
                return usuarioBC.salvar(Usuario(0, **request.json))
            else:
                return {"msg":"Os campos cpf e senha não podem ser vazios"}, 422
        else:
            return {"msg":"Parâmetro(s) ausente(s)"}, 422
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" in request.headers:
            if 'cpf' in request.json and 'nome' in request.json and 'email' in request.json and 'senha' in request.json:
                if request.json['cpf'] and request.json['nome'] and request.json['email'] and request.json['senha']:
                    usuarioBC = UsuarioBC()
                    return usuarioBC.atualizar(request.headers["Authorization"], Usuario(id, **request.json))
                else:
                    return {"msg":"Os campos cpf e senha não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            return usuarioBC.remover(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/logar", methods=['POST'])
def logar():
    try:
        if 'cpf' in request.json and 'senha' in request.json:
            cpf = ''.join(filter(str.isdigit, str(request.json['cpf'])))
            senha = request.json['senha']
            print({'cpf': cpf, 'senha': senha})
            if cpf and senha:
                usuarioBC = UsuarioBC()
                return usuarioBC.logar(cpf, senha)
            else:
                return {"msg":"Os campos cpf e senha não podem ser vazios"}, 422
        else:
            return {"msg":"Parâmetro(s) ausente(s)"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500

@usuarioRoutes.route("/api/v1/usuario/promover/<int:id>", methods=['POST'])
def promover(id):
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            return usuarioBC.promoverUsuario(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500
