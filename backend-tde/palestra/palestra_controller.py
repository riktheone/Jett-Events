import datetime
from evento.evento_dao import EventoDAO
from util.conversor_data import converterStringDataHoraParaData, converterStringDataParaData, converterStringDoBancoDataParaData
from palestra.palestra_dao import PalestraDAO
from flask import jsonify

from security.notations import loginRequired

class PalestraBC:

    def __init__(self):
        self.palestraDAO = PalestraDAO()

    @loginRequired
    def obterTodos(self, usuarioLogado):
        palestras = [{'id':tuplaPalestra[0], 'nome': tuplaPalestra[1], 'descricao': tuplaPalestra[2], 'dt_palestra': tuplaPalestra[3], 'horario_inicio_palestra': tuplaPalestra[4], 'horario_fim_palestra': tuplaPalestra[5], 'nome_palestrante': tuplaPalestra[6], 'minicurriculo_palestrante': tuplaPalestra[7], 'id_evento': tuplaPalestra[8]} for tuplaPalestra in self.palestraDAO.obterTodos()]
        return jsonify(palestras), 200

    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        palestraBanco = self.palestraDAO.obterPorId(id)
        if palestraBanco == None:
            return {"msg":"palestra não encontrada"}, 422
        return jsonify({'id':palestraBanco[0], 'nome': palestraBanco[1], 'descricao': palestraBanco[2], 'dt_palestra': palestraBanco[3], 'horario_inicio_palestra': palestraBanco[4], 'horario_fim_palestra': palestraBanco[5], 'nome_palestrante': palestraBanco[6], 'minicurriculo_palestrante': palestraBanco[7], 'id_evento': palestraBanco[8]}), 200

    @loginRequired
    def salvar(self, usuarioLogado, palestra):
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(palestra.id_evento) == None:
            return {"msg":"evento não existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode salvar uma palestra"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(palestra.dt_palestra):
            return {"msg":"Data de início da palestra precisa ser maior do que a data atual"}, 422
        if self.palestraDAO.salvar(palestra.nome, palestra.descricao, converterStringDataParaData(palestra.dt_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_inicio_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_fim_palestra), palestra.nome_palestrante, palestra.minicurriculo_palestrante, palestra.id_evento) > 0:
            return {"msg":"palestra criada com sucesso"}, 200
        return {"msg":"palestra não pôde ser criada"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, palestra):
        palestraBanco = self.palestraDAO.obterPorId(palestra.id)
        if palestraBanco == None:
            return {"msg":"palestra não encontrada"}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(palestra.id_evento) == None:
            return {"msg":"evento não existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode atualizar uma palestra"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(palestra.dt_palestra):
            return {"msg":"Data de início da palestra precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(palestraBanco[3]):
            return {"msg":"Prazo para atualizar palestra já foi encerrado"}, 422
        if self.palestraDAO.atualizar(palestra.id, palestra.nome, palestra.descricao, converterStringDataParaData(palestra.dt_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_inicio_palestra), converterStringDataHoraParaData(palestra.dt_palestra, palestra.horario_fim_palestra), palestra.nome_palestrante, palestra.minicurriculo_palestrante, palestra.id_evento) > 0:
            return {"msg":"palestra atualizada com sucesso"}, 200
        return {"msg":"palestra não pôde ser atualizada"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        palestraBanco = self.palestraDAO.obterPorId(id)
        if palestraBanco == None:
            return {"msg":"palestra não encontrada"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode remover uma palestra"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(palestraBanco[3]):
            return {"msg":"Prazo para remover palestra já foi encerrado"}, 422
        if self.palestraDAO.remover(id) > 0:
            return {"msg":"palestra removida com sucesso"}, 200
        return {"msg":"palestra não pôde ser removida"}, 500
    
    def obterPalestrasPorEvento(self, idEvento):
        return self.palestraDAO.obterPalestrasPorEvento(idEvento)