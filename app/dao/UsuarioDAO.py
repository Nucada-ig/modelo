import sqlite3

class UsuarioDAO:
    def __init__(self, db_path='app/database/usuarios.db'):
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
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, telefone, usuario, senha, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario.nome, usuario.email, usuario.telefone, usuario.usuario, usuario.senha, usuario.tipo))
        conn.commit()
        conn.close()

    def remover(self, id_usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conn.commit()
        conn.close()

    def procurar_um(self, id_usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id=?", (id_usuario,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        dados = cursor.fetchall()
        conn.close()
        return dados

