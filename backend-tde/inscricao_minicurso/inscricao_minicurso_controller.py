from inscricao_minicurso.inscricao_minicurso_dao import InscricaoMinicursoDAO

class InscricaoMinicursoBC:

    def __init__(self):
        self.inscricaoMinicursoDAO = InscricaoMinicursoDAO()

    def obterInscricoesPorUsuario(self, idUsuario):
        return self.inscricaoMinicursoDAO.obterInscricoesPorUsuario(idUsuario)
    
    def obterInscricoesPorMinicurso(self, idMinicurso):
        return self.inscricaoMinicursoDAO.obterInscricoesPorMinicurso(idMinicurso)
