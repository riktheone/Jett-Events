from flask import jsonify

from inscricao_evento.inscricao_evento_controller import InscricaoEventoBC
from inscricao_minicurso.inscricao_minicurso_controller import InscricaoMinicursoBC
from security.notations import loginRequired
from usuario.usuario_dao import UsuarioDAO
from util.cpf_util import limpar_cpf
from util.jwt_util import jwtEncode


class UsuarioBC:

    def __init__(self):
        self.usuarioDAO = UsuarioDAO()

    def obterUsuarioPorId(self, id):
        return self.usuarioDAO.obterPorId(id)

    def obterUsuarioPorCPF(self, cpf):
        return self.usuarioDAO.obterPorCPF(limpar_cpf(cpf))

    @loginRequired
    def obterTodos(self, usuarioLogado):
        usuarios = [
            {
                'id': tuplaUsuario[0],
                'cpf': tuplaUsuario[1],
                'nome': tuplaUsuario[2],
                'email': tuplaUsuario[3],
                'administrador': tuplaUsuario[4],
            }
            for tuplaUsuario in self.usuarioDAO.obterTodos()
        ]
        return jsonify(usuarios), 200

    def salvar(self, usuario):
        try:
            usuario.cpf = limpar_cpf(usuario.cpf)
            if len(usuario.cpf) != 11:
                return {"msg": "CPF deve conter 11 digitos"}, 422
            if self.usuarioDAO.obterPorCPF(usuario.cpf) is not None:
                return {"msg": f"Ja existe usuario cadastrado com o cpf {usuario.cpf}"}, 422
            if self.usuarioDAO.obterPorEmail(usuario.email) is not None:
                return {"msg": f"Ja existe usuario cadastrado com o e-mail {usuario.email}"}, 422
            if self.usuarioDAO.salvar(usuario.cpf, usuario.nome, usuario.email, usuario.senha) > 0:
                return {"msg": "Usuario salvo com sucesso"}, 200
            return {"msg": "Erro ao salvar usuario"}, 500
        except Exception as error:
            return {"msg": str(error)}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, usuario):
        try:
            usuarioBanco = self.usuarioDAO.obterPorId(usuario.id)
            if usuarioBanco is None:
                return {"msg": "Usuario nao encontrado"}, 422
            if not usuarioLogado.administrador and usuarioLogado.id != usuario.id:
                return {"msg": "Apenas o proprio usuario ou um administrador pode alterar seus dados"}, 422

            usuario.cpf = limpar_cpf(usuario.cpf)
            if usuarioBanco[1] != usuario.cpf:
                return {"msg": "Nao e possivel alterar o CPF do usuario"}, 422

            usuarioPorEmail = self.usuarioDAO.obterPorEmail(usuario.email)
            if usuarioPorEmail is not None and usuarioPorEmail[0] != usuario.id:
                return {"msg": f"Ja existe usuario cadastrado com o e-mail {usuario.email}"}, 422

            senha = usuario.senha
            if senha is None or senha == "" or senha == "sem_alteracao":
                senha = usuarioBanco[4]

            if self.usuarioDAO.atualizar(usuario.id, usuario.nome, usuario.email, senha) > 0:
                return {"msg": "Usuario atualizado com sucesso"}, 200
            return {"msg": "Erro ao atualizar usuario"}, 500
        except Exception as error:
            return {"msg": str(error)}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        try:
            if not usuarioLogado.administrador:
                return {"msg": "Apenas um usuario administrador pode remover um usuario"}, 422
            usuario = self.usuarioDAO.obterPorId(id)
            if usuario is None:
                return {"msg": "Usuario nao encontrado"}, 422
            inscricaoEventoBC = InscricaoEventoBC()
            inscricaoMinicursoBC = InscricaoMinicursoBC()
            if inscricaoEventoBC.obterInscricoesPorUsuario(id) is not None and len(inscricaoEventoBC.obterInscricoesPorUsuario(id)) > 0:
                return {"msg": "Usuario nao pode ser removido, pois ele esta inscrito em evento"}, 422
            if inscricaoMinicursoBC.obterInscricoesPorUsuario(id) is not None and len(inscricaoMinicursoBC.obterInscricoesPorUsuario(id)) > 0:
                return {"msg": "Usuario nao pode ser removido, pois ele esta inscrito em minicurso"}, 422
            if self.usuarioDAO.remover(id) > 0:
                return {"msg": "Usuario removido com sucesso"}, 200
            return {"msg": "Erro ao remover usuario"}, 500
        except Exception as error:
            return {"msg": str(error)}, 500

    def logar(self, cpf, senha):
        cpf_limpo = limpar_cpf(cpf)
        usuario = self.usuarioDAO.obterPorCPF(cpf_limpo)
        if usuario is None:
            return {"msg": "usuario invalido"}, 403
        if usuario[4].upper() == senha.upper():
            return {"token_jwt": jwtEncode(cpf_limpo)}, 200
        return {"msg": "senha invalida"}, 403

    @loginRequired
    def promoverUsuario(self, usuarioLogado, id):
        try:
            if not usuarioLogado.administrador:
                return {"msg": "Apenas um usuario administrador pode promover outro usuario a administrador"}, 422
            usuario = self.usuarioDAO.obterPorId(id)
            if usuario is None:
                return {"msg": "Usuario nao encontrado"}, 422
            if usuario[5] == True:
                return {"msg": "Usuario ja e administrador do sistema"}, 422
            if self.usuarioDAO.atualizarTipoUsuario(id) > 0:
                return {"msg": "Usuario promovido com sucesso"}, 200
            return {"msg": "Erro ao promover usuario"}, 500
        except Exception as error:
            return {"msg": str(error)}, 500
