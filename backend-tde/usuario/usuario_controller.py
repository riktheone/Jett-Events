
from flask import jsonify
from inscricao_evento.inscricao_evento_controller import InscricaoEventoBC
from inscricao_minicurso.inscricao_minicurso_controller import InscricaoMinicursoBC
from security.notations import loginRequired
from usuario.usuario_dao import UsuarioDAO
from util.jwt_util import jwtEncode

class UsuarioBC:

    def __init__(self):
        self.usuarioDAO = UsuarioDAO()

    def obterUsuarioPorId(self, id):
        return self.usuarioDAO.obterPorId(id)
    
    def obterUsuarioPorCPF(self, cpf):
        return self.usuarioDAO.obterPorCPF(cpf)

    @loginRequired
    def obterTodos(self, usuarioLogado):
        eventos = [{'id':tuplaUsuario[0], 'cpf': tuplaUsuario[1], 'nome': tuplaUsuario[2], 'email': tuplaUsuario[3], 'administrador': tuplaUsuario[4]} for tuplaUsuario in self.usuarioDAO.obterTodos()]
        return jsonify(eventos), 200

    def salvar(self, usuario):
        try:
            if self.usuarioDAO.obterPorCPF(usuario.cpf) != None:
                return {"msg":f"Já existe usuário cadastrado com o cpf {usuario.cpf}"}, 422
            if self.usuarioDAO.salvar(usuario.cpf, usuario.nome, usuario.email, usuario.senha) > 0:
                return {"msg":"Usuário salvo com sucesso"}, 200
            return {"msg":"Erro ao salvar usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500
    
    @loginRequired
    def atualizar(self, usuarioLogado, usuario):
        try:
            usuarioBanco = self.usuarioDAO.obterPorId(usuario.id)
            if usuarioBanco == None:
                return {"msg":"Usuário não encontrado"}, 422
            if not usuarioLogado.id == usuario.id:
                return {"msg":"Apenas o próprio usuário pode alterar seus dados"}, 422
            if usuarioBanco[1] != usuario.cpf:
                return {"msg":"Não é possível alterar o CPF do usuário"}, 422
            if self.usuarioDAO.atualizar(usuario.id, usuario.nome, usuario.email, usuario.senha) > 0:
                return {"msg":"Usuário atualizado com sucesso"}, 200
            return {"msg":"Erro ao atualizar usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500
    
    @loginRequired
    def remover(self, usuarioLogado, id):
        try:
            if not usuarioLogado.administrador:
                return {"msg":"Apenas um usuário administrador pode remover um usuário"}, 422
            usuario = self.usuarioDAO.obterPorId(id)
            if usuario == None:
                return {"msg":"Usuário não encontrado"}, 422
            inscricaoEventoBC = InscricaoEventoBC()
            inscricaoMinicursoBC = InscricaoMinicursoBC()
            if inscricaoEventoBC.obterInscricoesPorUsuario(id) != None and len(inscricaoEventoBC.obterInscricoesPorUsuario(id)) > 0:
                return {"msg":"Usuário não pode ser removido, pois ele está inscrito em evento"}, 422
            if inscricaoMinicursoBC.obterInscricoesPorUsuario(id) != None and len(inscricaoMinicursoBC.obterInscricoesPorUsuario(id)) > 0:
                return {"msg":"Usuário não pode ser removido, pois ele está inscrito em minicurso"}, 422
            if self.usuarioDAO.remover(id) > 0:
                return {"msg":"Usuário removido com sucesso"}, 200
            return {"msg":"Erro ao remover usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    def logar(self, cpf, senha):
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        usuario = self.usuarioDAO.obterPorCPF(cpf_limpo)
        if usuario == None:
            return {"msg":"usuario inválido"}, 403
        if usuario[4].upper() == senha.upper():
            return {"token_jwt":jwtEncode(cpf_limpo)}, 200
        return {"msg":"senha inválida"}, 403
    
    @loginRequired
    def promoverUsuario(self, usuarioLogado, id):
        try:
            if not usuarioLogado.administrador:
                return {"msg":"Apenas um usuário administrador pode promover outro usuário à administrador"}, 422
            usuario = self.usuarioDAO.obterPorId(id)
            if usuario == None:
                return {"msg":"Usuário não encontrado"}, 422
            if usuario[5] == True:
                return {"msg":"Usuário já é admnistrador do sistema"}, 422
            if self.usuarioDAO.atualizarTipoUsuario(id) > 0:
                return {"msg":"Usuário promovido com sucesso"}, 200
            return {"msg":"Erro ao promover usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500
    