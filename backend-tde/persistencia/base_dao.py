import sqlite3

class BaseDAO:

    def conectar(self):
        self.conn = sqlite3.connect("./database/tde.db")
        self.cur = self.conn.cursor()

    def desconectar(self):
        self.cur.close()
        self.conn.close()

    def obterRegistrosPorParametros(self, comandoSelect, parametros):
        self.conectar()
        self.cur.execute(comandoSelect, (parametros))
        lista = self.cur.fetchall()
        self.desconectar()
        return lista
    
    def obterRegistroPorParametro(self, comandoSelect, parametros):
        self.conectar()
        self.cur.execute(comandoSelect, (parametros))
        entidade = self.cur.fetchone()
        self.desconectar()
        return entidade

    def obterRegistros(self, comandoSelect):
        self.conectar()
        self.cur.execute(comandoSelect)
        lista = self.cur.fetchall()
        self.desconectar()
        return lista

    def executarComandoDML(self, comandoDML, parametros):
        self.conectar()
        linhasAfetadas = self.cur.execute(comandoDML, (parametros)).rowcount
        self.conn.commit()
        self.desconectar()
        return linhasAfetadas
