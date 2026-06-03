from usuario.usuario import Usuario
from usuario.usuario_dao import UsuarioDAO
from util.jwt_util import jwtDecode
from functools import wraps

def loginRequired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if len(args) > 1:
                decodedToken = jwtDecode(args[1])
                if not decodedToken:
                    return {"msg":"token inválido"}, 403
                if not "cpf" in decodedToken:
                    return {"msg":"token inválido"}, 403
                usuarioDAO = UsuarioDAO()
                tuplaUsuario = usuarioDAO.obterPorCPF(decodedToken["cpf"])
                dictUsuario = {"id":tuplaUsuario[0], "cpf":tuplaUsuario[1], "nome":tuplaUsuario[2], "email":tuplaUsuario[3], "senha":tuplaUsuario[4]}
                usuario = Usuario(** dictUsuario)
                usuario.id = tuplaUsuario[0]
                usuario.administrador = tuplaUsuario[5]
                new_args = list(args)
                new_args[1] = usuario
                args = tuple(new_args)
                return func(*args, **kwargs)
            return {"msg":"token ausente na requisição"}, 401
        except Exception as err:
            return {"msg":str(err)}, 401
    return wrapper
