from persistencia.base_dao import BaseDAO


class UsuarioDAO(BaseDAO):

    def obterTodos(self):
        return self.obterRegistros("select id, cpf, nome, email, usuario_admin from usuarios")
    
    def obterPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, cpf, nome, email, hash_senha, usuario_admin from usuarios where id = ?", parametros)

    def obterPorCPF(self, cpf):
        parametros = [cpf]
        return self.obterRegistroPorParametro("select id, cpf, nome, email, hash_senha, usuario_admin from usuarios where cpf = ?", parametros)
    
    def salvar(self, cpf, nome, email, senha):
        parametros = [cpf, nome, email, senha, False]
        return self.executarComandoDML("insert into usuarios (cpf, nome, email, hash_senha, usuario_admin) values (?, ?, ?, ?, ?)", parametros)
    
    def atualizar(self, id, nome, email, senha):
        parametros = [nome, email, senha, id]
        return self.executarComandoDML("update usuarios set nome = ?, email = ?, hash_senha = ? where id = ?", parametros)
    
    def remover(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from usuarios where id = ?", parametros)
    
    def atualizarTipoUsuario(self, id):
        parametros = [True, id]
        return self.executarComandoDML("update usuarios set usuario_admin = ? where id = ?", parametros)