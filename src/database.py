import sqlite3


class Database:

    def __init__(self, dbname):
        self.conn = sqlite3.connect(f"{dbname}.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("begin")
        self.create_table("contatos", [
            "id INTEGER PRIMARY KEY",
            "nome VARCHAR(100) NOT NULL",
            "recado VARCHAR(100)",
            "numero VARCHAR(30) NOT NULL",
            "step INTEGER DEFAULT 0 NOT NULL",
            "cotacao VARCHAR(15)"
        ], constraints={
            "UNIQUE(numero)"
        })

    def create_table(self, tablename, columns, constraints):
        query = f"CREATE TABLE IF NOT EXISTS {tablename} ({','.join(columns)}" + "".join([
            f",{i}" for i in constraints]) + ");"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_client(self, nome, recado, numero, tablename='contatos'):
        if not recado:
            recado = 'NULL'
        else:
            recado = f"'{recado}'"

        try:
            query = f"INSERT INTO {tablename} VALUES (NULL, '{nome}', {recado}, '{numero}', 0, NULL)"
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(e)

    def update_step(self, step, numero, tablename='contatos'):
        query = f"UPDATE {tablename} SET step = {step} WHERE numero = '{numero}'"
        self.cursor.execute(query)
        self.conn.commit()

    def update_cotacao(self, cotacao, numero, tablename='contatos'):
        query = f"UPDATE {tablename} SET cotacao = '{cotacao}' WHERE numero = '{numero}'"
        self.cursor.execute(query)
        self.conn.commit()

    def select_cotacao(self, numero, tablename='contatos'):
        query = f"SELECT cotacao FROM {tablename} WHERE numero = ? LIMIT 1"
        self.cursor.execute(query, [numero])
        return self.cursor.fetchone()

    def find_client(self, numero, tablename='contatos'):
        query = f"SELECT * FROM {tablename} WHERE numero = ? LIMIT 1"
        self.cursor.execute(query, [numero])
        return self.cursor.fetchone()
