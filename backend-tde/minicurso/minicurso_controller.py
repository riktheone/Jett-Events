import datetime
from util.conversor_data import converterStringDataParaData, converterStringDoBancoDataParaData
from evento.evento_dao import EventoDAO
from inscricao_minicurso.inscricao_minicurso_controller import InscricaoMinicursoBC
from minicurso.minicurso_dao import MinicursoDAO
from flask import jsonify

from security.notations import loginRequired
from usuario.usuario_controller import UsuarioBC

class MinicursoBC:

    def __init__(self):
        self.minicursoDAO = MinicursoDAO()

    @loginRequired
    def obterTodos(self, usuarioLogado):
        minicursos = [{'id':tuplaPalestra[0], 'nome': tuplaPalestra[1], 'descricao': tuplaPalestra[2], 'dt_minicurso': tuplaPalestra[3], 'horario_inicio_minicurso': tuplaPalestra[4], 'horario_fim_minicurso': tuplaPalestra[5], 'nome_instrutor': tuplaPalestra[6], 'minicurriculo_instrutor': tuplaPalestra[7], 'dt_limite_inscricao': tuplaPalestra[8], 'vagas_disponiveis': tuplaPalestra[9], 'id_evento': tuplaPalestra[10]} for tuplaPalestra in self.minicursoDAO.obterTodos()]
        return jsonify(minicursos), 200
    
    @loginRequired
    def obterPorId(self, usuarioLogado, id):
        minicursoBanco = self.minicursoDAO.obterPorId(id)
        if minicursoBanco == None:
            return {"msg":"minicurso não encontrado"}, 422
        return jsonify({'id':minicursoBanco[0], 'nome': minicursoBanco[1], 'descricao': minicursoBanco[2], 'dt_minicurso': minicursoBanco[3], 'horario_inicio_minicurso': minicursoBanco[4], 'horario_fim_minicurso': minicursoBanco[5], 'nome_instrutor': minicursoBanco[6], 'minicurriculo_instrutor': minicursoBanco[7], 'dt_limite_inscricao': minicursoBanco[8], 'vagas_disponiveis': minicursoBanco[9], 'id_evento': minicursoBanco[10]}), 200

    @loginRequired
    def salvar(self, usuarioLogado, minicurso):
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(minicurso.id_evento) == None:
            return {"msg":"evento não existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode salvar uma minicurso"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_minicurso):
            return {"msg":"Data de início do minicurso precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg":"Data limite para inscrição no minicurso precisa ser maior do que a data atual"}, 422
        if converterStringDataParaData(minicurso.dt_minicurso) <= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg":"Data limite para inscrição no minicurso precisa ser menor do que a data do minicurso"}, 422
        if self.minicursoDAO.salvar(minicurso.nome, minicurso.descricao, converterStringDataParaData(minicurso.dt_minicurso), minicurso.horario_inicio_minicurso, minicurso.horario_fim_minicurso, minicurso.nome_instrutor, minicurso.minicurriculo_instrutor, converterStringDataParaData(minicurso.dt_limite_inscricao), minicurso.vagas_disponiveis, minicurso.id_evento) > 0:
            return {"msg":"minicurso criado com sucesso"}, 200
        return {"msg":"minicurso não pôde ser criado"}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, minicurso):
        minicursoBanco = self.minicursoDAO.obterPorId(minicurso.id)
        if minicursoBanco == None:
            return {"msg":"minicurso não encontrado"}, 422
        eventoDAO = EventoDAO()
        if eventoDAO.obterPorId(minicurso.id_evento) == None:
            return {"msg":"evento não existe"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode atualizar um minicurso"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_minicurso):
            return {"msg":"Data de início do minicurso precisa ser maior do que a data atual"}, 422
        if datetime.datetime.now() >= converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg":"Data limite para inscrição no minicurso precisa ser maior do que a data atual"}, 422
        if converterStringDataParaData(minicurso.dt_minicurso) < converterStringDataParaData(minicurso.dt_limite_inscricao):
            return {"msg":"Data limite para inscrição no minicurso precisa ser menor do que a data do minicurso"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(minicursoBanco[3]):
            return {"msg":"Prazo para atualizar minicurso está encerrado"}, 422
        if self.minicursoDAO.atualizar(minicurso.id, minicurso.nome, minicurso.descricao, converterStringDataParaData(minicurso.dt_minicurso), minicurso.horario_inicio_minicurso, minicurso.horario_fim_minicurso, minicurso.nome_instrutor, minicurso.minicurriculo_instrutor, converterStringDataParaData(minicurso.dt_limite_inscricao), minicurso.vagas_disponiveis, minicurso.id_evento) > 0:
            return {"msg":"minicurso atualizado com sucesso"}, 200
        return {"msg":"minicurso não pôde ser atualizado"}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        minicursoBanco = self.minicursoDAO.obterPorId(id)
        if minicursoBanco == None:
            return {"msg":"minicurso não encontrado"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode remover um minicurso"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(minicursoBanco[3]):
            return {"Prazo para remover minicurso está encerrado"}, 422
        inscricaoMinicursoBC = InscricaoMinicursoBC()
        inscricoesMinicurso = inscricaoMinicursoBC.obterInscricoesPorMinicurso(id)
        if inscricoesMinicurso != None and len(inscricoesMinicurso) > 0:
            return {"msg":"Minicurso não pode ser removido, pois existem inscrições efetuadas"}, 422
        if self.minicursoDAO.remover(id) > 0:
            return {"msg":"minicurso removido com sucesso"}, 200
        return {"msg":"minicurso não pôde ser removido"}, 500
    
    def obterMinicursosPorEvento(self, idEvento):
        return self.minicursoDAO.obterMinicursosPorEvento(idEvento)
    
    @loginRequired
    def inscrever(self, usuarioLogado, id_minicurso, id_usuario_participante):
        minicursoBanco = self.minicursoDAO.obterPorId(id_minicurso)
        if minicursoBanco == None:
            return {"msg":"minicurso não encontrado"}, 422
        if usuarioLogado.id != int(id_usuario_participante):
            return {"msg":"usuário não pode inscrever outro usuário"}, 422
        if datetime.datetime.now() > converterStringDoBancoDataParaData(minicursoBanco[8]):
            return {"msg":"Prazo para inscrição encerrado"}, 422
        eventoDAO = EventoDAO()
        inscricaoEmEvento = eventoDAO.obterInscricaoEmEvento(minicursoBanco[10], id_usuario_participante)
        if inscricaoEmEvento == None or len(inscricaoEmEvento) <= 0:
            return {"msg":f"o usuário de id {id_usuario_participante} não está inscrito no evento de id = {minicursoBanco[10]} ao qual o minicurso faz parte"}, 422
        inscricaoEmMinicurso = self.minicursoDAO.obterInscricaoEmMinicurso(id_minicurso, id_usuario_participante)
        if inscricaoEmMinicurso != None and len(inscricaoEmMinicurso) > 0:
            return {"msg":f"o usuário de id {id_usuario_participante} já está inscrito no minicurso de id = {id_minicurso}"}, 422
        self.minicursoDAO.inscrever(id_minicurso, id_usuario_participante)
        return {"msg":"inscrição efetuada com sucesso"}, 200

    @loginRequired
    def removerInscricao(self, usuarioLogado, id_minicurso, id_participante):
        minicursoBanco = self.minicursoDAO.obterPorId(id_minicurso)
        if minicursoBanco == None:
            return {"msg":"minicurso não encontrado"}, 422
        if not usuarioLogado.administrador:
            return {"msg":"Apenas um usuário administrador pode remover uma inscrição em um minicurso"}, 422
        if datetime.datetime.now() >= converterStringDoBancoDataParaData(minicursoBanco[3]):
            return {"msg":"Prazo para remover inscrição encerrado"}, 422
        inscricaoEmMinicurso = self.minicursoDAO.obterInscricaoEmMinicurso(id_minicurso, id_participante)
        if inscricaoEmMinicurso == None or len(inscricaoEmMinicurso) <= 0:
            return {"msg":f"o usuário de id {id_participante} não está inscrito no minicurso de id = {id_minicurso}"}, 422
        self.minicursoDAO.removerInscricao(id_minicurso, id_participante)
        return {"msg":"inscrição removida com sucesso"}, 200
    
    @loginRequired
    def obterInscritosEmMinicurso(self, usuarioLogado, id):
        listaUsuariosInscritos = []
        inscricaoMinicursoBC = InscricaoMinicursoBC()
        inscricoesMinicurso = inscricaoMinicursoBC.obterInscricoesPorMinicurso(id)
        if inscricoesMinicurso == None or len(inscricoesMinicurso) <= 0:
            return jsonify(listaUsuariosInscritos), 200
        
        retorno = {"id_minicurso":id}
        usuarioBC = UsuarioBC()
        for inscricao in inscricoesMinicurso:
            usuarioInscrito = usuarioBC.obterUsuarioPorId(inscricao[0])
            if usuarioInscrito != None:
                retorno["id"] = usuarioInscrito[0]
                retorno["cpf"] = usuarioInscrito[1]
                retorno["nome"] = usuarioInscrito[2]
                retorno["email"] = usuarioInscrito[3]
                listaUsuariosInscritos.append(retorno)
        return jsonify(listaUsuariosInscritos), 200