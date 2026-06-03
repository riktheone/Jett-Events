from inscricao_evento.inscricao_evento_dao import InscricaoEventoDAO

class InscricaoEventoBC:

    def __init__(self):
        self.inscricaoEventoDAO = InscricaoEventoDAO()

    def obterInscricoesPorUsuario(self, idUsuario):
        return self.inscricaoEventoDAO.obterInscricoesPorUsuario(idUsuario)
    
    def obterInscricoesPorEvento(self, idEvento):
        return self.inscricaoEventoDAO.obterInscricoesPorEvento(idEvento)
