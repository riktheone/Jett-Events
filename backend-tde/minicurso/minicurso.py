class Minicurso:

    def __init__(self, id, nome, descricao, dt_minicurso, horario_inicio_minicurso, horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor, dt_limite_inscricao, numero_vagas, id_evento):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dt_minicurso = dt_minicurso
        self.horario_inicio_minicurso = horario_inicio_minicurso
        self.horario_fim_minicurso = horario_fim_minicurso
        self.nome_instrutor = nome_instrutor
        self.minicurriculo_instrutor = minicurriculo_instrutor
        self.dt_limite_inscricao = dt_limite_inscricao
        self.vagas_disponiveis= numero_vagas
        self.id_evento = id_evento
