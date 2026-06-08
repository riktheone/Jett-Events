from persistencia.base_dao import BaseDAO


class InscricaoMinicursoDAO(BaseDAO):

    def obterInscricoesPorUsuario(self, idUsuario):
        parametros = [idUsuario]
        return self.obterRegistrosPorParametros(
            """
            select id_usuario, id_minicurso, dt_inscricao, cpf_participante,
                   nome_participante, email_participante, telefone_participante
            from inscricao_minicurso
            where id_usuario = ?
            """,
            parametros,
        )

    def obterInscricoesPorMinicurso(self, idMinicurso):
        parametros = [idMinicurso]
        return self.obterRegistrosPorParametros(
            """
            select id_usuario, id_minicurso, dt_inscricao, cpf_participante,
                   nome_participante, email_participante, telefone_participante
            from inscricao_minicurso
            where id_minicurso = ?
            """,
            parametros,
        )
