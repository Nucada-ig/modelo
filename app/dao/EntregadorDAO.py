import sqlite3

class EntregadorDAO:
    def __init__(self, db_path='app/database/entregadores.db'):
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
            CREATE TABLE IF NOT EXISTS entregadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                veiculo TEXT NOT NULL,
                placa TEXT,
                status TEXT DEFAULT 'ativo',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, entregador):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entregadores (usuario_id, veiculo, placa, status)
            VALUES (?, ?, ?, ?)
        """, (entregador.usuario_id, entregador.veiculo, entregador.placa, entregador.status))
        conn.commit()
        conn.close()

    def remover(self, id_entregador):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entregadores WHERE id=?", (id_entregador,))
        conn.commit()
        conn.close()

    def procurar_um(self, id_entregador):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entregadores WHERE id=?", (id_entregador,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entregadores")
        dados = cursor.fetchall()
        conn.close()
        return dados

