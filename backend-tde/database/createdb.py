import sqlite3

DATABASE_FILE="./database/tde.db"

# conectando...
conn = sqlite3.connect(DATABASE_FILE)

# definindo um cursor
cursor = conn.cursor()

# criando as tabelas

cursor.execute("""
CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cpf VARCHAR(11) NOT NULL,
  email VARCHAR(30) NOT NULL,
  nome VARCHAR(50) NOT NULL,
  usuario_admin BOOLEAN NOT NULL,
  hash_senha VARCHAR(20) NOT NULL
);
""")
print('Tabela usuarios criada com sucesso.')

cursor.execute("""
CREATE TABLE eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  dt_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  dt_fim TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  dt_limite_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  vagas_disponiveis INTEGER NOT NULL,
  nome_responsavel VARCHAR(50) NOT NULL,
  cpf_responsavel VARCHAR(50) NOT NULL,
  email_responsavel VARCHAR(50) NOT NULL  
);
""")
print('Tabela evento criada com sucesso.')

cursor.execute("""
CREATE TABLE palestras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  dt_palestra TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  horario_inicio_palestra TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  horario_fim_palestra TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  nome_palestrante VARCHAR(50) NOT NULL,
  minicurriculo_palestrante VARCHAR(512) NOT NULL,
  id_evento INTEGER NOT NULL,
  FOREIGN KEY (id_evento) REFERENCES eventos(id)
);
""")
print('Tabela palestras criada com sucesso.')


cursor.execute("""
CREATE TABLE minicursos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(100) NOT NULL,
  dt_minicurso TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  horario_inicio_minicurso TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  horario_fim_minicurso TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  nome_instrutor VARCHAR(50) NOT NULL,
  minicurriculo_instrutor VARCHAR(512) NOT NULL,
  dt_limite_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  vagas_disponiveis INTEGER NOT NULL,
  id_evento INTEGER NOT NULL,
  FOREIGN KEY (id_evento) REFERENCES eventos(id)
);
""")
print('Tabela palestras criada com sucesso.')

cursor.execute("""
CREATE TABLE inscricao_evento (
  id_usuario INTEGER,
  id_evento INTEGER,
  dt_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT inscricao_evento_pk PRIMARY KEY (id_usuario, id_evento),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
  FOREIGN KEY (id_evento) REFERENCES eventos(id)
);
""")
print('Tabela inscricao_evento criada com sucesso.')

cursor.execute("""
CREATE TABLE inscricao_minicurso (
  id_usuario INTEGER,
  id_minicurso INTEGER,
  dt_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT inscricao_minicurso_pk PRIMARY KEY (id_usuario, id_minicurso),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
  FOREIGN KEY (id_minicurso) REFERENCES minicurso(id)
);
""")
print('Tabela inscricao_minicurso criada com sucesso.')

conn.commit()
# desconectando...
conn.close()
