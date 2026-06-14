import sqlite3
import hashlib

DATABASE_FILE = "./database/tde.db"

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest().upper()

admin = {
    "cpf": "1234",
    "nome": "Super Admin",
    "email": "admin@jett-events.local",
    "senha": "adminpw",
    "usuario_admin": True
}

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cpf_existente = cursor.execute("SELECT id FROM usuarios WHERE cpf = ?", (admin["cpf"],)).fetchone()
if cpf_existente:
    print(f"Super usuario com CPF {admin['cpf']} ja existe, pulando.")
else:
    cursor.execute(
        "INSERT INTO usuarios (cpf, nome, email, hash_senha, usuario_admin) VALUES (?, ?, ?, ?, ?)",
        (admin["cpf"], admin["nome"], admin["email"], hash_senha(admin["senha"]), admin["usuario_admin"])
    )
    conn.commit()
    print(f"Super usuario '{admin['nome']}' inserido com sucesso.")
    print(f"  CPF:   {admin['cpf']}")
    print(f"  Senha: {admin['senha']}")

conn.close()
