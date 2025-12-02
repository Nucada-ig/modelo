import sqlite3

class EnderecoDAO:
    def __init__(self, db_path='app/database/app.db'):
        self.db_path = db_path
        self._criar_tabela()

    def _conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _criar_tabela(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                rua TEXT NOT NULL,
                numero TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT NOT NULL,
                complemento TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, endereco):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO enderecos (usuario_id, rua, numero, cidade, estado, cep, complemento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (endereco.usuario_id, endereco.rua, endereco.numero, endereco.cidade, endereco.estado, endereco.cep, endereco.complemento))
        conn.commit()
        conn.close()

    def remover(self, id_endereco):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enderecos WHERE id=?", (id_endereco,))
        conn.commit()
        conn.close()

    def procurar_um(self, id_endereco):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enderecos WHERE id=?", (id_endereco,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enderecos")
        dados = cursor.fetchall()
        conn.close()
        return dados

