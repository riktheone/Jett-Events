import sqlite3

DATABASE_FILE = "./database/tde.db"


def column_exists(cursor, table, column):
    rows = cursor.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row[1] == column for row in rows)


def index_exists(cursor, index_name):
    rows = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND name = ?", (index_name,)).fetchall()
    return len(rows) > 0


conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

for table in ("inscricao_evento", "inscricao_minicurso"):
    columns = {
        "cpf_participante": "VARCHAR(11)",
        "nome_participante": "VARCHAR(50)",
        "email_participante": "VARCHAR(50)",
        "telefone_participante": "VARCHAR(20)",
    }
    for column, definition in columns.items():
        if not column_exists(cursor, table, column):
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

if not index_exists(cursor, "idx_usuarios_cpf_unique"):
    cursor.execute("CREATE UNIQUE INDEX idx_usuarios_cpf_unique ON usuarios(cpf)")

if not index_exists(cursor, "idx_usuarios_email_unique"):
    cursor.execute("CREATE UNIQUE INDEX idx_usuarios_email_unique ON usuarios(lower(email))")

cursor.execute("""
    UPDATE inscricao_evento
    SET cpf_participante = coalesce(cpf_participante, (SELECT cpf FROM usuarios WHERE usuarios.id = inscricao_evento.id_usuario)),
        nome_participante = coalesce(nome_participante, (SELECT nome FROM usuarios WHERE usuarios.id = inscricao_evento.id_usuario)),
        email_participante = coalesce(email_participante, (SELECT email FROM usuarios WHERE usuarios.id = inscricao_evento.id_usuario)),
        telefone_participante = coalesce(telefone_participante, '')
""")

cursor.execute("""
    UPDATE inscricao_minicurso
    SET cpf_participante = coalesce(cpf_participante, (SELECT cpf FROM usuarios WHERE usuarios.id = inscricao_minicurso.id_usuario)),
        nome_participante = coalesce(nome_participante, (SELECT nome FROM usuarios WHERE usuarios.id = inscricao_minicurso.id_usuario)),
        email_participante = coalesce(email_participante, (SELECT email FROM usuarios WHERE usuarios.id = inscricao_minicurso.id_usuario)),
        telefone_participante = coalesce(telefone_participante, '')
""")

conn.commit()
conn.close()

print("Migracao concluida.")
