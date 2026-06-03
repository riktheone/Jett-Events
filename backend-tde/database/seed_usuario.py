import sqlite3
import hashlib

DATABASE_FILE = "./database/tde.db"

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest().upper()

usuarios = [
    {
        "cpf": "12345678901",
        "nome": "João da Silva",
        "email": "joao.silva@email.com",
        "senha": "senha123",
        "usuario_admin": False
    }
]

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

for u in usuarios:
    cpf_existente = cursor.execute("SELECT id FROM usuarios WHERE cpf = ?", (u["cpf"],)).fetchone()
    if cpf_existente:
        print(f"Usuário com CPF {u['cpf']} já existe, pulando.")
        continue

    cursor.execute(
        "INSERT INTO usuarios (cpf, nome, email, hash_senha, usuario_admin) VALUES (?, ?, ?, ?, ?)",
        (u["cpf"], u["nome"], u["email"], hash_senha(u["senha"]), u["usuario_admin"])
    )
    print(f"Usuário '{u['nome']}' inserido com sucesso.")
    print(f"  CPF:   {u['cpf']}")
    print(f"  Email: {u['email']}")
    print(f"  Senha: {u['senha']}")

conn.commit()
conn.close()
