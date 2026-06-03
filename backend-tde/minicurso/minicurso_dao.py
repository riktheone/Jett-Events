import datetime
from persistencia.base_dao import BaseDAO


class MinicursoDAO(BaseDAO):

    def obterTodos(self):
        return self.obterRegistros("select id, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento from minicursos")

    def obterMinicursosPorEvento(self, idEvento):
        parametros = [idEvento]
        return self.obterRegistrosPorParametros("select id, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento from minicursos where id_evento = ?", parametros)
    
    def obterPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento from minicursos where id = ?", parametros)
    
    def salvar(self, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento):
        parametros = [nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento]
        return self.executarComandoDML("insert into minicursos (nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", parametros)
    
    def atualizar(self, id, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento):
        parametros = [nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, vagas_disponiveis, id_evento, id]
        return self.executarComandoDML("update minicursos set nome = ?, descricao = ?, dt_minicurso = ?, horario_inicio_minicurso = ?, horario_fim_minicurso = ?, nome_instrutor = ?, minicurriculo_instrutor = ?,  dt_limite_inscricao = ?, vagas_disponiveis = ?, id_evento = ? where id = ?", parametros)
    
    def remover(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from minicursos where id = ?", parametros)
    
    def inscrever(self, id_minicurso, id_usuario_participante):
        parametros = [id_minicurso, id_usuario_participante, datetime.datetime.now().strftime("%d/%m/%Y")]
        return self.executarComandoDML("insert into inscricao_minicurso (id_minicurso, id_usuario, dt_inscricao) values (?, ?, ?)", parametros)
    
    def obterInscricaoEmMinicurso(self, id_minicurso, id_participante):
        parametros = [id_minicurso, id_participante]
        return self.obterRegistrosPorParametros("select id_usuario, id_minicurso, dt_inscricao from inscricao_minicurso where id_minicurso = ? and id_usuario = ?", parametros)
    
    def removerInscricao(self, id_minicurso, id_participante):
        parametros = [id_minicurso, id_participante]
        return self.executarComandoDML("delete from inscricao_minicurso where id_minicurso = ? and id_usuario = ?", parametros)
