from persistencia.base_dao import BaseDAO


class PalestraDAO(BaseDAO):

    def obterTodos(self):
        return self.obterRegistros("select id, nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento from palestras")

    def obterPalestrasPorEvento(self, idEvento):
        parametros = [idEvento]
        return self.obterRegistrosPorParametros("select id, nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento from palestras where id_evento = ?", parametros)
    
    def obterPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento from palestras where id = ?", parametros)
    
    def salvar(self, nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento):
        parametros = [nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento]
        return self.executarComandoDML("insert into palestras (nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento) values (?, ?, ?, ?, ?, ?, ?, ?)", parametros)
    
    def atualizar(self, id, nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento):
        parametros = [nome, descricao, dt_palestra, horario_inicio_palestra, horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento, id]
        return self.executarComandoDML("update palestras set nome = ?, descricao = ?, dt_palestra = ?, horario_inicio_palestra = ?, horario_fim_palestra = ?, nome_palestrante = ?, minicurriculo_palestrante = ?, id_evento = ? where id = ?", parametros)
    
    def remover(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from palestras where id = ?", parametros)
