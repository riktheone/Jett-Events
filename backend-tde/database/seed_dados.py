import sqlite3

DATABASE_FILE = "./database/tde.db"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# ── Eventos ──────────────────────────────────────────────────────────────────

eventos = [
    (
        "Semana de Tecnologia 2026",
        "Evento anual de tecnologia com palestras e minicursos.",
        "2026-07-14 08:00:00", "2026-07-18 18:00:00", "2026-07-10 23:59:00",
        200, "Prof. Carlos Mendes", "11122233344", "carlos.mendes@unifan.br"
    ),
    (
        "Hackathon ADS 2026",
        "Maratona de programacao para alunos de ADS.",
        "2026-08-05 08:00:00", "2026-08-06 20:00:00", "2026-08-01 23:59:00",
        80, "Prof. Ana Lima", "55566677788", "ana.lima@unifan.br"
    ),
]

for ev in eventos:
    cursor.execute("""
        INSERT INTO eventos (nome, descricao, dt_inicio, dt_fim, dt_limite_inscricao,
                             vagas_disponiveis, nome_responsavel, cpf_responsavel, email_responsavel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ev)

ids_eventos = [row[0] for row in cursor.execute("SELECT id FROM eventos ORDER BY id")]
id_evento1 = ids_eventos[-2]
id_evento2 = ids_eventos[-1]
print(f"Eventos inseridos: IDs {id_evento1} e {id_evento2}")

# ── Palestras ─────────────────────────────────────────────────────────────────

palestras = [
    (
        "Inteligencia Artificial na Pratica",
        "Como aplicar IA em projetos reais do mercado.",
        "2026-07-14", "08:00:00", "09:30:00",
        "Dr. Ricardo Souza",
        "Doutor em Computacao pela USP, pesquisador de IA com 15 anos de experiencia.",
        id_evento1
    ),
    (
        "Desenvolvimento Web Moderno",
        "Tendencias e ferramentas do desenvolvimento web em 2026.",
        "2026-07-15", "10:00:00", "11:30:00",
        "Fernanda Costa",
        "Engenheira de software senior, especialista em arquiteturas front-end.",
        id_evento1
    ),
    (
        "Seguranca da Informacao",
        "Principais ameacas e como proteger sistemas corporativos.",
        "2026-07-16", "14:00:00", "15:30:00",
        "Marcos Oliveira",
        "Especialista em ciberseguranca com certificacoes CISSP e CEH.",
        id_evento1
    ),
    (
        "Pitch de Projetos",
        "Como apresentar seu projeto para investidores.",
        "2026-08-05", "09:00:00", "10:00:00",
        "Juliana Alves",
        "Empreendedora serial, fundadora de duas startups de tecnologia.",
        id_evento2
    ),
]

cursor.executemany("""
    INSERT INTO palestras (nome, descricao, dt_palestra, horario_inicio_palestra,
                           horario_fim_palestra, nome_palestrante, minicurriculo_palestrante, id_evento)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", palestras)
print(f"Palestras inseridas: {len(palestras)}")

# ── Minicursos ────────────────────────────────────────────────────────────────

minicursos = [
    (
        "Python para Iniciantes",
        "Introducao pratica a linguagem Python com exercicios.",
        "2026-07-14", "13:00:00", "17:00:00",
        "Beatriz Ramos",
        "Desenvolvedora Python com 8 anos de experiencia em back-end.",
        "2026-07-10 23:59:00", 30, id_evento1
    ),
    (
        "React do Zero",
        "Construindo interfaces modernas com React e hooks.",
        "2026-07-15", "13:00:00", "17:00:00",
        "Lucas Ferreira",
        "Front-end developer, contribuidor ativo de projetos open source.",
        "2026-07-10 23:59:00", 25, id_evento1
    ),
    (
        "Banco de Dados SQL e NoSQL",
        "Diferencas, casos de uso e pratica com SQLite e MongoDB.",
        "2026-07-17", "08:00:00", "12:00:00",
        "Patricia Nunes",
        "DBA com experiencia em empresas de grande porte no setor financeiro.",
        "2026-07-10 23:59:00", 20, id_evento1
    ),
    (
        "Git e GitHub na Equipe",
        "Fluxos de trabalho colaborativos com Git para times ageis.",
        "2026-08-05", "13:00:00", "17:00:00",
        "Rafael Dias",
        "Engenheiro DevOps, instrutor certificado GitHub.",
        "2026-08-01 23:59:00", 40, id_evento2
    ),
]

cursor.executemany("""
    INSERT INTO minicursos (nome, descricao, dt_minicurso, horario_inicio_minicurso,
                            horario_fim_minicurso, nome_instrutor, minicurriculo_instrutor,
                            dt_limite_inscricao, vagas_disponiveis, id_evento)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", minicursos)
print(f"Minicursos inseridos: {len(minicursos)}")

conn.commit()
conn.close()
print("Seed concluido com sucesso.")
