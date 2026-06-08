import datetime

from flask import jsonify

from evento.evento_dao import EventoDAO
from inscricao_minicurso.inscricao_minicurso_controller import InscricaoMinicursoBC
from minicurso.minicurso_dao import MinicursoDAO
from security.notations import loginRequired
from usuario.usuario_controller import UsuarioBC
from util.conversor_data import converterStringDataHoraParaData, converterStringDataParaData, converterStringDoBancoDataParaData
from util.cpf_util import limpar_cpf


class MinicursoBC:

    def __init__(self):
        self.minicursoDAO = MinicursoDAO()

    def __minicursoParaJson(self, tuplaMinicurso):
        return {
            'id': tuplaMinicurso[0],
            'nome': tuplaMinicurso[1],
            'descricao': tuplaMinicurso[2],
            'dt_minicurso': tuplaMinicurso[3],
            'horario_inicio_minicurso': tuplaMinicurso[4],
            'horario_fim_minicurso': tuplaMinicurso[5],
            'nome_instrutor': tuplaMinicurso[6],
            'minicurriculo_instrutor': tuplaMinicurso[7],
            'dt_limite_inscricao': tuplaMinicurso[8],
            'numero_vagas': tuplaMinicurso[9],
            'id_evento': tuplaMinicurso[10],
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

    def __validarCamposObrigatorios(self, minicurso):
        campos = [
            minicurso.id_evento,
            minicurso.nome,
            minicurso.descricao,
            minicurso.dt_minicurso,
            minicurso.horario_inicio_minicurso,
            minicurso.horario_fim_minicurso,
            minicurso.nome_instrutor,
            minicurso.minicurriculo_instrutor,
            minicurso.dt_limite_inscricao,
            minicurso.numero_vagas,
        ]
        if any(str(campo or "").strip() == "" for campo in campos):
            return False, "Todos os campos do minicurso sao obrigatorios"
        if int(minicurso.numero_vagas) <= 0:
            return False, "Numero de vagas deve ser maior que zero"
        return True, ""

    @loginRequired
    def obterTodos(self, usuarioLogado):
        return jsonify([self.__minicursoParaJson(m) for m in self.minicursoDAO.obterTodos()]), 200

    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        minicursoBanco = self.minicursoDAO.obterPorId(id)
        if minicursoBanco is None:
            return {"msg": "minicurso nao encontrado"}, 422
        return jsonify(self.__minicursoParaJson(minicursoBanco)), 200

    @loginRequired
    def salvar(self, usuarioLogado, minicurso):
        validou, mensagem = self.__validarCamposObrigatorios(minicurso)
        if not validou:
            return {"msg": mensagem}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(minicurso.id_evento) is None:
            return {"msg": "evento nao existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode salvar um minicurso"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_minicurso):
            return {"msg": "Data de inicio do minicurso precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg": "Data limite para inscricao no minicurso precisa ser maior do que a data atual"}, 422
        if converterStringDataParaData(minicurso.dt_minicurso) <= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg": "Data limite para inscricao no minicurso precisa ser menor do que a data do minicurso"}, 422
        if self.minicursoDAO.salvar(minicurso.nome, minicurso.descricao, converterStringDataParaData(minicurso.dt_minicurso), converterStringDataHoraParaData(minicurso.dt_minicurso, minicurso.horario_inicio_minicurso), converterStringDataHoraParaData(minicurso.dt_minicurso, minicurso.horario_fim_minicurso), minicurso.nome_instrutor, minicurso.minicurriculo_instrutor, converterStringDataParaData(minicurso.dt_limite_inscricao), minicurso.numero_vagas, minicurso.id_evento) > 0:
            return {"msg": "minicurso criado com sucesso"}, 200
        return {"msg": "minicurso nao pode ser criado"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, minicurso):
        validou, mensagem = self.__validarCamposObrigatorios(minicurso)
        if not validou:
            return {"msg": mensagem}, 422
        minicursoBanco = self.minicursoDAO.obterPorId(minicurso.id)
        if minicursoBanco is None:
            return {"msg": "minicurso nao encontrado"}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(minicurso.id_evento) is None:
            return {"msg": "evento nao existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode atualizar um minicurso"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(minicursoBanco[3]):
            return {"msg": "Prazo para atualizar minicurso esta encerrado"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_minicurso):
            return {"msg": "Data de inicio do minicurso precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg": "Data limite para inscricao no minicurso precisa ser maior do que a data atual"}, 422
        if converterStringDataParaData(minicurso.dt_minicurso) <= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg": "Data limite para inscricao no minicurso precisa ser menor do que a data do minicurso"}, 422
        if self.minicursoDAO.atualizar(minicurso.id, minicurso.nome, minicurso.descricao, converterStringDataParaData(minicurso.dt_minicurso), converterStringDataHoraParaData(minicurso.dt_minicurso, minicurso.horario_inicio_minicurso), converterStringDataHoraParaData(minicurso.dt_minicurso, minicurso.horario_fim_minicurso), minicurso.nome_instrutor, minicurso.minicurriculo_instrutor, converterStringDataParaData(minicurso.dt_limite_inscricao), minicurso.numero_vagas, minicurso.id_evento) > 0:
            return {"msg": "minicurso atualizado com sucesso"}, 200
        return {"msg": "minicurso nao pode ser atualizado"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        minicursoBanco = self.minicursoDAO.obterPorId(id)
        if minicursoBanco is None:
            return {"msg": "minicurso nao encontrado"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode remover um minicurso"}, 422
        eventoBanco = EventoDAO().obterPorId(minicursoBanco[10])
        if eventoBanco is not None and datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg": "Prazo para remover minicurso esta encerrado"}, 422
        inscricoesMinicurso = InscricaoMinicursoBC().obterInscricoesPorMinicurso(id)
        if inscricoesMinicurso is not None and len(inscricoesMinicurso) > 0:
            return {"msg": "Minicurso nao pode ser removido, pois existem inscricoes efetuadas"}, 422
        if self.minicursoDAO.remover(id) > 0:
            return {"msg": "minicurso removido com sucesso"}, 200
        return {"msg": "minicurso nao pode ser removido"}, 500

    def obterMinicursosPorEvento(self, idEvento):
        return self.minicursoDAO.obterMinicursosPorEvento(idEvento)

    @loginRequired
    def inscrever(self, usuarioLogado, id_minicurso, participante):
        minicursoBanco = self.minicursoDAO.obterPorId(id_minicurso)
        if minicursoBanco is None:
            return {"msg": "minicurso nao encontrado"}, 422
        validou, mensagem, dados = self.__normalizarParticipante(usuarioLogado, participante)
        if not validou:
            return {"msg": mensagem}, 422
        if datetime.datetime.now() > converterStringDoBancoDataParaData(minicursoBanco[8]):
            return {"msg": "Prazo para inscricao encerrado"}, 422
        eventoDAO = EventoDAO()
        inscricaoEmEvento = eventoDAO.obterInscricaoEmEvento(minicursoBanco[10], usuarioLogado.id)
        if inscricaoEmEvento is None or len(inscricaoEmEvento) <= 0:
            return {"msg": f"o usuario de id {usuarioLogado.id} nao esta inscrito no evento de id = {minicursoBanco[10]} ao qual o minicurso faz parte"}, 422
        inscricoesMinicurso = InscricaoMinicursoBC().obterInscricoesPorMinicurso(id_minicurso)
        if len(inscricoesMinicurso) >= int(minicursoBanco[9]):
            return {"msg": "Nao ha vagas disponiveis para este minicurso"}, 422
        inscricaoEmMinicurso = self.minicursoDAO.obterInscricaoEmMinicurso(id_minicurso, usuarioLogado.id)
        if inscricaoEmMinicurso is not None and len(inscricaoEmMinicurso) > 0:
            return {"msg": f"o usuario de id {usuarioLogado.id} ja esta inscrito no minicurso de id = {id_minicurso}"}, 422
        self.minicursoDAO.inscrever(id_minicurso, usuarioLogado.id, dados)
        return {"msg": "inscricao efetuada com sucesso"}, 200

    @loginRequired
    def removerInscricao(self, usuarioLogado, id_minicurso, id_participante):
        minicursoBanco = self.minicursoDAO.obterPorId(id_minicurso)
        if minicursoBanco is None:
            return {"msg": "minicurso nao encontrado"}, 422
        if not usuarioLogado.administrador and usuarioLogado.id != int(id_participante):
            return {"msg": "Apenas o proprio usuario ou um administrador pode remover a inscricao"}, 422
        inicio = converterStringDataHoraParaData(minicursoBanco[3], minicursoBanco[4])
        limite = inicio - datetime.timedelta(hours=24)
        if datetime.datetime.now() > limite:
            return {"msg": "Prazo para remover inscricao encerrado"}, 422
        inscricaoEmMinicurso = self.minicursoDAO.obterInscricaoEmMinicurso(id_minicurso, id_participante)
        if inscricaoEmMinicurso is None or len(inscricaoEmMinicurso) <= 0:
            return {"msg": f"o usuario de id {id_participante} nao esta inscrito no minicurso de id = {id_minicurso}"}, 422
        self.minicursoDAO.removerInscricao(id_minicurso, id_participante)
        return {"msg": "inscricao removida com sucesso"}, 200

    @loginRequired
    def obterInscritosEmMinicurso(self, usuarioLogado, id):
        inscricoesMinicurso = InscricaoMinicursoBC().obterInscricoesPorMinicurso(id)
        return jsonify([self.__participanteParaJson(inscricao) for inscricao in inscricoesMinicurso]), 200
