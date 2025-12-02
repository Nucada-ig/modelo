import sqlite3
from datetime import datetime

class AplicanteDAO:
    def __init__(self, db_path='app/database/app.db'):
        self.db_path = db_path
        self._criar_tabela()

    def _conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    #tabela
    def _criar_tabela(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aplicantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo_aplicacao TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente',
                data_envio TEXT
            );
        """)
        conn.commit()
        conn.close()

    #inserir
    def inserir(self, nome, email, telefone, usuario, senha, tipo_aplicacao):
        conn = self._conectar()
        cursor = conn.cursor()
        data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
                INSERT INTO aplicantes (nome, email, telefone, usuario, senha, tipo_aplicacao, status, data_envio)
                VALUES (?, ?, ?, ?, ?, ?, 'pendente', ?)
            """, (nome, email, telefone, usuario, senha, tipo_aplicacao, data_envio))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Erro ao inserir aplicante:", e)
            conn.rollback()
            conn.close()
            return False

    #selecionar um só
    def buscar_um(self, aplicante_id):
        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM aplicantes WHERE id=?", (aplicante_id,))
        dado = cursor.fetchone()

        conn.close()
        return dado

    #selecionar todos
    def buscar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM aplicantes")
        dados = cursor.fetchall()

        conn.close()
        return dados

    #deletar aplicante
    def remover(self, aplicante_id):
        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM aplicantes WHERE id=?", (aplicante_id,))
        conn.commit()
        removido = cursor.rowcount > 0

        conn.close()
        return removido

    #aprovar aplicante
    def aprovar(self, aplicante_id):
        conn = self._conectar()
        cursor = conn.cursor()

        # Buscar aplicante
        cursor.execute("SELECT * FROM aplicantes WHERE id=?", (aplicante_id,))
        aplicante = cursor.fetchone()

        if not aplicante:
            conn.close()
            return False

        # Campos do aplicante
        id_, nome, email, telefone, usuario, senha, tipo_aplicacao, _, _ = aplicante

        try:
            # Se for entregador -> cria na tabela entregadores
            if tipo_aplicacao.lower() == "entregador":
                cursor.execute("""
                    INSERT INTO entregadores (nome, email, telefone, usuario, senha)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, email, telefone, usuario, senha))

            # Caso contrário -> vira usuário normal
            else:
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, telefone, usuario, senha, tipo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nome, email, telefone, usuario, senha, tipo_aplicacao))

            # Apagamos o aplicante após aprovação
            cursor.execute("DELETE FROM aplicantes WHERE id=?", (aplicante_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print("Erro ao aprovar aplicante:", e)
            conn.rollback()
            conn.close()
            return False

    # rejeitar aplicante
    def rejeitar(self, aplicante_id):
        conn = self._conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM aplicantes WHERE id=?", (aplicante_id,))
            conn.commit()
            removido = cursor.rowcount > 0

            conn.close()
            return removido

        except Exception as e:
            print("Erro ao rejeitar aplicante:", e)
            conn.rollback()
            conn.close()
            return False


