import datetime
from inscricao_evento.inscricao_evento_controller import InscricaoEventoBC
from minicurso.minicurso_controller import MinicursoBC
from minicurso.minicurso_dao import MinicursoDAO
from palestra.palestra_controller import PalestraBC
from usuario.usuario_controller import UsuarioBC
from util.conversor_data import converterStringDataParaData, converterStringDoBancoDataParaData
from evento.evento_dao import EventoDAO
from flask import jsonify

from security.notations import loginRequired

class EventoBC:

    def __init__(self):
        self.eventoDAO = EventoDAO()

    def __validarDatas(self, evento):
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_inicio):
            return False, "Data de início do evento precisa ser maior do que a data atual"
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_fim):
            return False, "Data de fim do evento precisa ser maior do que a data atual"
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_limite_inscricao):
            return False, "Data limite para inscrição precisa ser maior do que a data atual"
        if converterStringDataParaData(evento.dt_inicio) > converterStringDataParaData(evento.dt_fim):
            return False, "Data de início do evento precisa ser anterior ou igual a data fim do evento"
        if converterStringDataParaData(evento.dt_limite_inscricao) > converterStringDataParaData(evento.dt_inicio):
            return False, "Data limite para inscrição do evento precisa ser anterior ou igual a data de início do evento"
        return True, ""

    @loginRequired
    def obterProgramacao(self, usuarioLogado, idEvento):
        retorno = {"id_evento": idEvento}
        palestraBC = PalestraBC()
        minicursoBC = MinicursoBC()
        palestras = [{'id':tuplaPalestra[0], 'nome': tuplaPalestra[1], 'descricao': tuplaPalestra[2], 'dt_palestra': tuplaPalestra[3], 'horario_inicio_palestra': tuplaPalestra[4], 'horario_fim_palestra': tuplaPalestra[5], 'nome_palestrante': tuplaPalestra[6], 'minicurriculo_palestrante': tuplaPalestra[7], 'id_evento': tuplaPalestra[8]} for tuplaPalestra in palestraBC.obterPalestrasPorEvento(idEvento)]
        minicursos = [{'id':tuplaPalestra[0], 'nome': tuplaPalestra[1], 'descricao': tuplaPalestra[2], 'dt_minicurso': tuplaPalestra[3], 'horario_inicio_minicurso': tuplaPalestra[4], 'horario_fim_minicurso': tuplaPalestra[5], 'nome_instrutor': tuplaPalestra[6], 'minicurriculo_instrutor': tuplaPalestra[7], 'dt_limite_inscricao': tuplaPalestra[8], 'vagas_disponiveis': tuplaPalestra[9], 'id_evento': tuplaPalestra[10]} for tuplaPalestra in minicursoBC.obterMinicursosPorEvento(idEvento)]
        retorno["palestras"] = palestras
        retorno["minicursos"] = minicursos
        return jsonify(retorno)

    @loginRequired
    def obterTodosPorPeriodo(self, usuarioLogado, dtInicio, dtFim):
        eventos = [{'id':tuplaEvento[0], 'nome': tuplaEvento[1], 'descricao': tuplaEvento[2], 'dt_inicio': tuplaEvento[3], 'dt_fim': tuplaEvento[4], 'dt_limite_inscricao': tuplaEvento[5], 'numero_vagas': tuplaEvento[6], 'cpf_responsavel': tuplaEvento[7], 'nome_responsavel': tuplaEvento[8], 'email_responsavel': tuplaEvento[9]} for tuplaEvento in self.eventoDAO.obterTodosPorPeriodo(converterStringDataParaData(dtInicio), converterStringDataParaData(dtFim))]
        return jsonify(eventos), 200

    @loginRequired
    def obterTodos(self, usuarioLogado):
        eventos = [{'id':tuplaEvento[0], 'nome': tuplaEvento[1], 'descricao': tuplaEvento[2], 'dt_inicio': tuplaEvento[3], 'dt_fim': tuplaEvento[4], 'dt_limite_inscricao': tuplaEvento[5], 'numero_vagas': tuplaEvento[6], 'cpf_responsavel': tuplaEvento[7], 'nome_responsavel': tuplaEvento[8], 'email_responsavel': tuplaEvento[9]} for tuplaEvento in self.eventoDAO.obterTodos()]
        return jsonify(eventos), 200
    
    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        eventoBanco = self.eventoDAO.obterPorId(id)
        if eventoBanco == None:
            return {"msg":"evento não encontrado"}, 422
        return jsonify({'id':eventoBanco[0], 'nome': eventoBanco[1], 'descricao': eventoBanco[2], 'dt_inicio': eventoBanco[3], 'dt_fim': eventoBanco[4], 'dt_limite_inscricao': eventoBanco[5], 'numero_vagas': eventoBanco[6], 'cpf_responsavel': eventoBanco[7], 'nome_responsavel': eventoBanco[8], 'email_responsavel': eventoBanco[9]}), 200

    @loginRequired
    def obterInscritosEmEvento(self, usuarioLogado, id):
        listaUsuariosInscritos = []
        inscricaoEventoBC = InscricaoEventoBC()
        inscricoesEvento = inscricaoEventoBC.obterInscricoesPorEvento(id)
        if inscricoesEvento == None or len(inscricoesEvento) <= 0:
            return jsonify(listaUsuariosInscritos), 200
        
        retorno = {"id_evento":id}
        usuarioBC = UsuarioBC()
        for inscricao in inscricoesEvento:
            usuarioInscrito = usuarioBC.obterUsuarioPorId(inscricao[0])
            if usuarioInscrito != None:
                retorno["id"] = usuarioInscrito[0]
                retorno["cpf"] = usuarioInscrito[1]
                retorno["nome"] = usuarioInscrito[2]
                retorno["email"] = usuarioInscrito[3]
                listaUsuariosInscritos.append(retorno)
        return jsonify(listaUsuariosInscritos), 200

    @loginRequired
    def inscrever(self, usuarioLogado, id_evento, id_usuario_participante):
        eventoBanco = self.eventoDAO.obterPorId(id_evento)
        if eventoBanco == None:
            return {"msg":"evento não encontrado"}, 422
        if usuarioLogado.id != int(id_usuario_participante):
            return {"msg":"usuário não pode inscrever outro usuário"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[5]):
            return {"msg":"Prazo para inscrição encerrado"}, 422
        inscricaoEmEvento = self.eventoDAO.obterInscricaoEmEvento(id_evento, id_usuario_participante)
        if inscricaoEmEvento != None and len(inscricaoEmEvento) > 0:
            return {"msg":f"o usuário de id {id_usuario_participante} já está inscrito no evento de id = {id_evento}"}, 422
        self.eventoDAO.inscrever(id_evento, id_usuario_participante)
        return {"msg":"inscrição efetuada com sucesso"}, 200

    @loginRequired
    def removerInscricao(self, usuarioLogado, id_evento, id_participante):
        eventoBanco = self.eventoDAO.obterPorId(id_evento)
        if eventoBanco == None:
            return {"msg":"evento não encontrado"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode remover uma inscrição em um evento"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg":"Prazo para remover inscrição encerrado"}, 422
        inscricaoEmEvento = self.eventoDAO.obterInscricaoEmEvento(id_evento, id_participante)
        if inscricaoEmEvento == None or len(inscricaoEmEvento) <= 0:
            return {"msg":f"o usuário de id {id_participante} não está inscrito no evento de id = {id_evento}"}, 422
        minicursoDAO = MinicursoDAO()
        minicursos = minicursoDAO.obterMinicursosPorEvento(id_evento)
        for minicurso in minicursos:
            inscricaoParticipanteEmMinicurso = minicursoDAO.obterInscricaoEmMinicurso(minicurso[0], id_participante)
            if inscricaoParticipanteEmMinicurso != None and len(inscricaoParticipanteEmMinicurso)>0:
                return {"msg":"Não é possível remover a participação do participante neste evento, pois ele está inscrito em minicursos do evento"}, 422
        self.eventoDAO.removerInscricao(id_evento, id_participante)
        return {"msg":"inscrição removida com sucesso"}, 200

    @loginRequired
    def salvar(self, usuarioLogado, evento):
        validou, mensagem = self.__validarDatas(evento)
        if not validou:
            return {"msg":mensagem}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode criar um evento"}, 422
        if self.eventoDAO.salvar(evento.nome, evento.descricao, converterStringDataParaData(evento.dt_inicio), converterStringDataParaData(evento.dt_fim), converterStringDataParaData(evento.dt_limite_inscricao), evento.numero_vagas, evento.cpf_responsavel, evento.nome_responsavel, evento.email_responsavel) > 0:
            return {"msg":"evento criado com sucesso"}, 200
        return {"msg":"evento não pôde ser criado"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, evento):
        eventoBanco = self.eventoDAO.obterPorId(evento.id)
        if eventoBanco == None:
            return {"msg":"evento não encontrado"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg":"Prazo para atualizar o evento já está encerrado"}, 422
        validou, mensagem = self.__validarDatas(evento)
        if not validou:
            return {"msg":mensagem}, 422        
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode atualizar um evento"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(evento.dt_inicio):
            return {"msg":"Prazo para alteração expirado"}, 422
        if self.eventoDAO.atualizar(evento.id, evento.nome, evento.descricao, converterStringDataParaData(evento.dt_inicio), converterStringDataParaData(evento.dt_fim), converterStringDataParaData(evento.dt_limite_inscricao), evento.numero_vagas, evento.cpf_responsavel, evento.nome_responsavel, evento.email_responsavel) > 0:
            return {"msg":"evento atualizado com sucesso"}, 200
        return {"msg":"evento não pôde ser atualizado"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):

        eventoBanco = self.eventoDAO.obterPorId(id)
        if eventoBanco == None:
            return {"msg":"evento não encontrado"}, 422

        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg":"Prazo para remoção expirado"}, 422

        inscricaoEventoBC = InscricaoEventoBC()
        inscricoesEvento = inscricaoEventoBC.obterInscricoesPorEvento(id)
        if inscricoesEvento != None and len(inscricoesEvento) > 0:
            return {"msg":"Evento não pode ser removido, pois existem inscrições efetuadas"}, 422
        
        palestraBC = PalestraBC()
        palestrasEvento = palestraBC.obterPalestrasPorEvento(id)
        if palestrasEvento != None and len(palestrasEvento) > 0:
            return {"msg":"Evento não pode ser removido, pois existem palestras cadastradas"}, 422
        
        minicursoBC = MinicursoBC()
        minicursosEvento = minicursoBC.obterMinicursosPorEvento(id)
        if minicursosEvento != None and len(minicursosEvento) > 0:
            return {"msg":"Evento não pode ser removido, pois existem minicursos cadastrados"}, 422

        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode remover um evento"}, 422

        if datetime.datetime.now() >= converterStringDoBancoDataParaData(eventoBanco[3]):
            return {"msg":"Prazo para remover o evento já está encerrado"}, 422

        if self.eventoDAO.remover(id) > 0:
            return {"msg":"evento removido com sucesso"}, 200
        return {"msg":"evento não pôde ser removido"}, 500