from persistencia.base_dao import BaseDAO


class InscricaoEventoDAO(BaseDAO):

    def obterInscricoesPorUsuario(self, idUsuario):
        parametros = [idUsuario]
        return self.obterRegistrosPorParametros("select id_usuario, id_evento, dt_inscricao from inscricao_evento where id_usuario = ?", parametros)


    def obterInscricoesPorEvento(self, idEvento):
        parametros = [idEvento]
        return self.obterRegistrosPorParametros("select id_usuario, id_evento, dt_inscricao from inscricao_evento where id_evento = ?", parametros)