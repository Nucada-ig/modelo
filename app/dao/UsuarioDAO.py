import sqlite3
import os
import time

class UsuarioDAO:
    def __init__(self, db_path='app/database/app.db'):
        self.db_path = db_path
        print(f"UsuarioDAO using db_path: {self.db_path}")
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
                cpf TEXT,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                username TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                restaurante_id INTEGER,
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, usuario):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = self._conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuarios (nome, cpf, email, telefone, username, senha, tipo, restaurante_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (usuario.nome, usuario.cpf, usuario.email, usuario.telefone, usuario.username, usuario.senha, usuario.tipo, usuario.restaurante_id))
                conn.commit()
                usuario_id = cursor.lastrowid
                conn.close()
                return usuario_id
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    conn.close()
                    raise e

    def remover(self, id_usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conn.commit()
        conn.close()

    def buscar_por_username(self, usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (usuario,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def buscar_por_id(self, id_usuario):
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

    def username_existe(self, username):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe

