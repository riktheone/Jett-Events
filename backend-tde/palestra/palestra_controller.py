import datetime

from flask import jsonify

from evento.evento_dao import EventoDAO
from palestra.palestra_dao import PalestraDAO
from security.notations import loginRequired
from util.conversor_data import converterStringDataHoraParaData, converterStringDataParaData, converterStringDoBancoDataParaData


class PalestraBC:

    def __init__(self):
        self.palestraDAO = PalestraDAO()

    def __palestraParaJson(self, tuplaPalestra):
        return {
            'id': tuplaPalestra[0],
            'nome': tuplaPalestra[1],
            'descricao': tuplaPalestra[2],
            'dt_palestra': tuplaPalestra[3],
            'horario_inicio_palestra': tuplaPalestra[4],
            'horario_fim_palestra': tuplaPalestra[5],
            'nome_palestrante': tuplaPalestra[6],
            'minicurriculo_palestrante': tuplaPalestra[7],
            'id_evento': tuplaPalestra[8],
        }

    def __validarCamposObrigatorios(self, palestra):
        campos = [
            palestra.id_evento,
            palestra.nome,
            palestra.descricao,
            palestra.dt_palestra,
            palestra.horario_inicio_palestra,
            palestra.horario_fim_palestra,
            palestra.nome_palestrante,
            palestra.minicurriculo_palestrante,
        ]
        if any(str(campo or "").strip() == "" for campo in campos):
            return False, "Todos os campos da palestra sao obrigatorios"
        return True, ""

    @loginRequired
    def obterTodos(self, usuarioLogado):
        return jsonify([self.__palestraParaJson(p) for p in self.palestraDAO.obterTodos()]), 200

    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        palestraBanco = self.palestraDAO.obterPorId(id)
        if palestraBanco is None:
            return {"msg": "palestra nao encontrada"}, 422
        return jsonify(self.__palestraParaJson(palestraBanco)), 200

    @loginRequired
    def salvar(self, usuarioLogado, palestra):
        validou, mensagem = self.__validarCamposObrigatorios(palestra)
        if not validou:
            return {"msg": mensagem}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(palestra.id_evento) is None:
            return {"msg": "evento nao existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode salvar uma palestra"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(palestra.dt_palestra):
            return {"msg": "Data de inicio da palestra precisa ser maior do que a data atual"}, 422
        if self.palestraDAO.salvar(palestra.nome, palestra.descricao, converterStringDataParaData(palestra.dt_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_inicio_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_fim_palestra), palestra.nome_palestrante, palestra.minicurriculo_palestrante, palestra.id_evento) > 0:
            return {"msg": "palestra criada com sucesso"}, 200
        return {"msg": "palestra nao pode ser criada"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, palestra):
        validou, mensagem = self.__validarCamposObrigatorios(palestra)
        if not validou:
            return {"msg": mensagem}, 422
        palestraBanco = self.palestraDAO.obterPorId(palestra.id)
        if palestraBanco is None:
            return {"msg": "palestra nao encontrada"}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(palestra.id_evento) is None:
            return {"msg": "evento nao existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode atualizar uma palestra"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(palestra.dt_palestra):
            return {"msg": "Data de inicio da palestra precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(palestraBanco[3]):
            return {"msg": "Prazo para atualizar palestra ja foi encerrado"}, 422
        if self.palestraDAO.atualizar(palestra.id, palestra.nome, palestra.descricao, converterStringDataParaData(palestra.dt_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_inicio_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_fim_palestra), palestra.nome_palestrante, palestra.minicurriculo_palestrante, palestra.id_evento) > 0:
            return {"msg": "palestra atualizada com sucesso"}, 200
        return {"msg": "palestra nao pode ser atualizada"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        palestraBanco = self.palestraDAO.obterPorId(id)
        if palestraBanco is None:
            return {"msg": "palestra nao encontrada"}, 422
        if not usuarioLogado.administrador:
            return {"msg": "Apenas um usuario administrador pode remover uma palestra"}, 422
        eventoBanco = EventoDAO().obterPorId(palestraBanco[8])
        if eventoBanco is not None and datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg": "Prazo para remover palestra ja foi encerrado"}, 422
        if self.palestraDAO.remover(id) > 0:
            return {"msg": "palestra removida com sucesso"}, 200
        return {"msg": "palestra nao pode ser removida"}, 500

    def obterPalestrasPorEvento(self, idEvento):
        return self.palestraDAO.obterPalestrasPorEvento(idEvento)
