import datetime

from flask import jsonify

from evento.evento_dao import EventoDAO
from inscricao_evento.inscricao_evento_controller import InscricaoEventoBC
from minicurso.minicurso_controller import MinicursoBC
from minicurso.minicurso_dao import MinicursoDAO
from palestra.palestra_controller import PalestraBC
from security.notations import loginRequired
from usuario.usuario_controller import UsuarioBC
from util.conversor_data import converterStringDataParaData, converterStringDoBancoDataParaData
from util.cpf_util import limpar_cpf


class EventoBC:

    def __init__(self):
        self.eventoDAO = EventoDAO()

    def __eventoParaJson(self, tuplaEvento):
        return {
            'id': tuplaEvento[0],
            'nome': tuplaEvento[1],
            'descricao': tuplaEvento[2],
            'dt_inicio': tuplaEvento[3],
            'dt_fim': tuplaEvento[4],
            'dt_limite_inscricao': tuplaEvento[5],
            'numero_vagas': tuplaEvento[6],
            'cpf_responsavel': tuplaEvento[7],
            'nome_responsavel': tuplaEvento[8],
            'email_responsavel': tuplaEvento[9],
        }

    def __participanteParaJson(self, inscricao):
        usuario = UsuarioBC().obterUsuarioPorId(inscricao[0])
        return {
            "id": inscricao[0],
            "cpf": inscricao[3] or (usuario[1] if usuario else ""),
            "nome": inscricao[4] or (usuario[2] if usuario else ""),
            "email": inscricao[5] or (usuario[3] if usuario else ""),
            "telefone": inscricao[6] or "",
            "dt_inscricao": inscricao[2],
        }

    def __normalizarParticipante(self, usuarioLogado, participante):
        dados = {
            "cpf_participante": limpar_cpf(participante.get("cpf_participante", "")),
            "nome_participante": str(participante.get("nome_participante", "")).strip(),
            "email_participante": str(participante.get("email_participante", "")).strip(),
            "telefone_participante": str(participante.get("telefone_participante", "")).strip(),
        }
        if len(dados["cpf_participante"]) != 11:
            return False, "CPF do participante deve conter 11 digitos", dados
        if not dados["nome_participante"] or not dados["email_participante"] or not dados["telefone_participante"]:
            return False, "Informe nome, e-mail e telefone do participante", dados
        if dados["cpf_participante"] != limpar_cpf(usuarioLogado.cpf):
            return False, "Usuario comum so pode realizar a propria inscricao", dados
        return True, "", dados

    def __validarDatas(self, evento):
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_inicio):
            return False, "Data de inicio do evento precisa ser maior do que a data atual"
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_fim):
            return False, "Data de fim do evento precisa ser maior do que a data atual"
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_limite_inscricao):
            return False, "Data limite para inscricao precisa ser maior do que a data atual"
        if converterStringDataParaData(evento.dt_inicio) > converterStringDataParaData(evento.dt_fim):
            return False, "Data de inicio do evento precisa ser anterior ou igual a data fim do evento"
        if converterStringDataParaData(evento.dt_limite_inscricao) > converterStringDataParaData(evento.dt_inicio):
            return False, "Data limite para inscricao do evento precisa ser anterior ou igual a data de inicio do evento"
        return True, ""

    def __validarCamposObrigatorios(self, evento):
        campos = [
            evento.nome,
            evento.descricao,
            evento.dt_inicio,
            evento.dt_fim,
            evento.dt_limite_inscricao,
            evento.numero_vagas,
            evento.cpf_responsavel,
            evento.nome_responsavel,
            evento.email_responsavel,
        ]
        if any(str(campo or "").strip() == "" for campo in campos):
            return False, "Todos os campos do evento sao obrigatorios"
        evento.cpf_responsavel = limpar_cpf(evento.cpf_responsavel)
        if len(evento.cpf_responsavel) != 11:
            return False, "CPF do responsavel deve conter 11 digitos"
        if int(evento.numero_vagas) <= 0:
            return False, "Numero de vagas deve ser maior que zero"
        return True, ""

    @loginRequired
    def obterProgramacao(self, usuarioLogado, idEvento):
        palestraBC = PalestraBC()
        minicursoBC = MinicursoBC()
        palestras = [
            {
                'id': p[0], 'nome': p[1], 'descricao': p[2], 'dt_palestra': p[3],
                'horario_inicio_palestra': p[4], 'horario_fim_palestra': p[5],
                'nome_palestrante': p[6], 'minicurriculo_palestrante': p[7],
                'id_evento': p[8],
            }
            for p in palestraBC.obterPalestrasPorEvento(idEvento)
        ]
        minicursos = [
            {
                'id': m[0], 'nome': m[1], 'descricao': m[2], 'dt_minicurso': m[3],
                'horario_inicio_minicurso': m[4], 'horario_fim_minicurso': m[5],
                'nome_instrutor': m[6], 'minicurriculo_instrutor': m[7],
                'dt_limite_inscricao': m[8], 'numero_vagas': m[9], 'id_evento': m[10],
            }
            for m in minicursoBC.obterMinicursosPorEvento(idEvento)
        ]
        return jsonify({"id_evento": idEvento, "palestras": palestras, "minicursos": minicursos}), 200

    @loginRequired
    def obterTodosPorPeriodo(self, usuarioLogado, dtInicio, dtFim):
        eventos = [
            self.__eventoParaJson(tuplaEvento)
            for tuplaEvento in self.eventoDAO.obterTodosPorPeriodo(
                converterStringDataParaData(dtInicio),
                converterStringDataParaData(dtFim),
            )
        ]
        return jsonify(eventos), 200

    @loginRequired
    def obterTodos(self, usuarioLogado):
        eventos = [self.__eventoParaJson(tuplaEvento) for tuplaEvento in self.eventoDAO.obterTodos()]
        return jsonify(eventos), 200

    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        eventoBanco = self.eventoDAO.obterPorId(id)
        if eventoBanco is None:
            return {"msg": "evento nao encontrado"}, 422
        return jsonify(self.__eventoParaJson(eventoBanco)), 200

    @loginRequired
    def obterInscritosEmEvento(self, usuarioLogado, id):
        inscricoesEvento = InscricaoEventoBC().obterInscricoesPorEvento(id)
        return jsonify([self.__participanteParaJson(inscricao) for inscricao in inscricoesEvento]), 200

    @loginRequired
    def inscrever(self, usuarioLogado, id_evento, participante):
        eventoBanco = self.eventoDAO.obterPorId(id_evento)
        if eventoBanco is None:
            return {"msg": "evento nao encontrado"}, 422
        validou, mensagem, dados = self.__normalizarParticipante(usuarioLogado, participante)
        if not validou:
            return {"msg": mensagem}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[5]):
            return {"msg": "Prazo para inscricao encerrado"}, 422
        inscricoesEvento = InscricaoEventoBC().obterInscricoesPorEvento(id_evento)
        if len(inscricoesEvento) >= int(eventoBanco[6]):
            return {"msg": "Nao ha vagas disponiveis para este evento"}, 422
        inscricaoEmEvento = self.eventoDAO.obterInscricaoEmEvento(id_evento, usuarioLogado.id)
        if inscricaoEmEvento is not None and len(inscricaoEmEvento) > 0:
            return {"msg": f"o usuario de id {usuarioLogado.id} ja esta inscrito no evento de id = {id_evento}"}, 422
        self.eventoDAO.inscrever(id_evento, usuarioLogado.id, dados)
        return {"msg": "inscricao efetuada com sucesso"}, 200

    @loginRequired
    def removerInscricao(self, usuarioLogado, id_evento, id_participante):
        eventoBanco = self.eventoDAO.obterPorId(id_evento)
        if eventoBanco is None:
            return {"msg": "evento nao encontrado"}, 422
        if not usuarioLogado.administrador and usuarioLogado.id != int(id_participante):
            return {"msg": "Apenas o proprio usuario ou um administrador pode remover a inscricao"}, 422
        limite = converterStringDoBancoDataParaData(eventoBanco[3]) - datetime.timedelta(hours=24)
        if datetime.datetime.now() > limite:
            return {"msg": "Prazo para remover inscricao encerrado"}, 422
        inscricaoEmEvento = self.eventoDAO.obterInscricaoEmEvento(id_evento, id_participante)
        if inscricaoEmEvento is None or len(inscricaoEmEvento) <= 0:
            return {"msg": f"o usuario de id {id_participante} nao esta inscrito no evento de id = {id_evento}"}, 422
        minicursoDAO = MinicursoDAO()
        minicursos = minicursoDAO.obterMinicursosPorEvento(id_evento)
        for minicurso in minicursos:
            inscricaoParticipanteEmMinicurso = minicursoDAO.obterInscricaoEmMinicurso(minicurso[0], id_participante)
            if inscricaoParticipanteEmMinicurso is not None and len(inscricaoParticipanteEmMinicurso) > 0:
                return {"msg": "Nao e possivel remover a inscricao no evento, pois o participante esta inscrito em minicursos do evento"}, 422
        self.eventoDAO.removerInscricao(id_evento, id_participante)
        return {"msg": "inscricao removida com sucesso"}, 200

    @loginRequired
    def salvar(self, usuarioLogado, evento):
        validou, mensagem = self.__validarCamposObrigatorios(evento)
        if not validou:
            return {"msg": mensagem}, 422
        validou, mensagem = self.__validarDatas(evento)
        if not validou:
            return {"msg": mensagem}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode criar um evento"}, 422
        if self.eventoDAO.salvar(evento.nome, evento.descricao, converterStringDataParaData(evento.dt_inicio), converterStringDataParaData(evento.dt_fim), converterStringDataParaData(evento.dt_limite_inscricao), evento.numero_vagas, evento.cpf_responsavel, evento.nome_responsavel, evento.email_responsavel) > 0:
            return {"msg": "evento criado com sucesso"}, 200
        return {"msg": "evento nao pode ser criado"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, evento):
        eventoBanco = self.eventoDAO.obterPorId(evento.id)
        if eventoBanco is None:
            return {"msg": "evento nao encontrado"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg": "Prazo para atualizar o evento ja esta encerrado"}, 422
        validou, mensagem = self.__validarCamposObrigatorios(evento)
        if not validou:
            return {"msg": mensagem}, 422
        validou, mensagem = self.__validarDatas(evento)
        if not validou:
            return {"msg": mensagem}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode atualizar um evento"}, 422
        if self.eventoDAO.atualizar(evento.id, evento.nome, evento.descricao, converterStringDataParaData(evento.dt_inicio), converterStringDataParaData(evento.dt_fim), converterStringDataParaData(evento.dt_limite_inscricao), evento.numero_vagas, evento.cpf_responsavel, evento.nome_responsavel, evento.email_responsavel) > 0:
            return {"msg": "evento atualizado com sucesso"}, 200
        return {"msg": "evento nao pode ser atualizado"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        eventoBanco = self.eventoDAO.obterPorId(id)
        if eventoBanco is None:
            return {"msg": "evento nao encontrado"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode remover um evento"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg": "Prazo para remocao expirado"}, 422
        inscricoesEvento = InscricaoEventoBC().obterInscricoesPorEvento(id)
        if inscricoesEvento is not None and len(inscricoesEvento) > 0:
            return {"msg": "Evento nao pode ser removido, pois existem inscricoes efetuadas"}, 422
        palestrasEvento = PalestraBC().obterPalestrasPorEvento(id)
        if palestrasEvento is not None and len(palestrasEvento) > 0:
            return {"msg": "Evento nao pode ser removido, pois existem palestras cadastradas"}, 422
        minicursosEvento = MinicursoBC().obterMinicursosPorEvento(id)
        if minicursosEvento is not None and len(minicursosEvento) > 0:
            return {"msg": "Evento nao pode ser removido, pois existem minicursos cadastrados"}, 422
        if self.eventoDAO.remover(id) > 0:
            return {"msg": "evento removido com sucesso"}, 200
        return {"msg": "evento nao pode ser removido"}, 500
