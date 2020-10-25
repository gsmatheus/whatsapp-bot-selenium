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
            "step INTEGER DEFAULT 0 NOT NULL"
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
            query = f"INSERT INTO {tablename} VALUES (NULL, '{nome}', {recado}, '{numero}', 0)"
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(e)

    def update_step(self, step, numero, tablename='contatos'):
        query = f"UPDATE {tablename} SET step = {step} WHERE numero = '{numero}'"
        self.cursor.execute(query)
        self.conn.commit()

    def find_client(self, numero, tablename='contatos'):
        query = f"SELECT * FROM {tablename} WHERE numero = ? LIMIT 1"
        self.cursor.execute(query, [numero])
        res = self.cursor.fetchone()
        if res:
            return {
                'nome': res[1],
                'recado': res[2],
                'numero': res[3],
                'step': res[4]
            }
