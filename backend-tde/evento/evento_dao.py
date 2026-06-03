import datetime
from persistencia.base_dao import BaseDAO


class EventoDAO(BaseDAO):

    def obterTodosPorPeriodo(self, dtInicio, dtFim):
        parametros = [dtInicio, dtFim]
        return self.obterRegistrosPorParametros("select id, nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao, vagas_disponiveis, cpf_responsavel, nome_responsavel, email_responsavel from eventos where dt_inicio >= ? and dt_inicio <= ?", parametros)

    def obterTodos(self):
        return self.obterRegistros("select id, nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao, vagas_disponiveis, cpf_responsavel, nome_responsavel, email_responsavel from eventos")
    
    def obterPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao, vagas_disponiveis, cpf_responsavel, nome_responsavel, email_responsavel from eventos where id = ?", parametros)
    
    def salvar(self, nome, descricao, dtInicio, dtFim, dtLimiteInscricao, vagasDisponiveis, cpfResponsavel, nomeResponsavel, emailResponsavel):
        parametros = [nome, descricao, dtInicio, dtFim, dtLimiteInscricao, vagasDisponiveis, cpfResponsavel, nomeResponsavel, emailResponsavel]
        return self.executarComandoDML("insert into eventos (nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao, vagas_disponiveis, cpf_responsavel, nome_responsavel, email_responsavel) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", parametros)
    
    def atualizar(self, id, nome, descricao, dtInicio, dtFim, dtLimiteInscricao, vagasDisponiveis, cpfResponsavel, nomeResponsavel, emailResponsavel):
        parametros = [nome, descricao, dtInicio, dtFim, dtLimiteInscricao, vagasDisponiveis, cpfResponsavel, nomeResponsavel, emailResponsavel, id]
        return self.executarComandoDML("update eventos set nome = ?, descricao = ?, dt_inicio = ?, dt_fim = ?, dt_limite_inscricao = ?, vagas_disponiveis = ?, cpf_responsavel = ?, nome_responsavel = ?, email_responsavel = ? where id = ?", parametros)
    
    def remover(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from eventos where id = ?", parametros)
    
    def inscrever(self, id_evento, id_usuario_participante):
        parametros = [id_evento, id_usuario_participante, datetime.datetime.now().strftime("%d/%m/%Y")]
        return self.executarComandoDML("insert into inscricao_evento (id_evento, id_usuario, dt_inscricao) values (?, ?, ?)", parametros)
    
    def obterInscricaoEmEvento(self, id_evento, id_participante):
        parametros = [id_evento, id_participante]
        return self.obterRegistrosPorParametros("select id_usuario, id_evento, dt_inscricao from inscricao_evento where id_evento = ? and id_usuario = ?", parametros)
    
    def removerInscricao(self, id_evento, id_participante):
        parametros = [id_evento, id_participante]
        return self.executarComandoDML("delete from inscricao_evento where id_evento = ? and id_usuario = ?", parametros)