import sqlite3

class RestauranteDAO:
    def __init__(self, db_path='app/database/restaurantes.db'):
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
            CREATE TABLE IF NOT EXISTS restaurantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                categoria TEXT,
                cnpj TEXT UNIQUE NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, restaurante):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO restaurantes (nome, descricao, categoria, cnpj, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """, (restaurante.nome, restaurante.descricao, restaurante.categoria, restaurante.cnpj, restaurante.usuario_id))
        conn.commit()
        conn.close()

    def remover(self, id_restaurante):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurantes WHERE id=?", (id_restaurante,))
        conn.commit()
        conn.close()

    def procurar_um(self, id_restaurante):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurantes WHERE id=?", (id_restaurante,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM restaurantes")
        dados = cursor.fetchall()
        conn.close()
        return dados

