class Evento:
    def __init__(self, id, nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao, numero_vagas, cpf_responsavel, nome_responsavel, email_responsavel):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dt_inicio = dt_inicio
        self.dt_fim = dt_fim
        self.dt_limite_inscricao = dt_limite_inscricao
        self.numero_vagas = numero_vagas
        self.cpf_responsavel = cpf_responsavel
        self.nome_responsavel = nome_responsavel
        self.email_responsavel = email_responsavel
