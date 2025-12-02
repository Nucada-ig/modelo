import sqlite3

class PratoDAO:
    def __init__(self, db_path='app/database/pratos.db'):
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
            CREATE TABLE IF NOT EXISTS pratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurante_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                categoria TEXT,
                disponivel INTEGER DEFAULT 1,
                tempo_preparo INTEGER,
                destaque INTEGER DEFAULT 0,
                imagem TEXT,
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, prato):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pratos (restaurante_id, nome, descricao, preco, categoria, disponivel, tempo_preparo, destaque, imagem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (prato.restaurante_id, prato.nome, prato.descricao, prato.preco, prato.categoria, prato.disponivel, prato.tempo_preparo, prato.destaque, prato.imagem))
        conn.commit()
        conn.close()

    def remover(self, id_prato):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pratos WHERE id=?", (id_prato,))
        conn.commit()
        conn.close()

    def atualizar_status(self, id_prato, disponivel):
        """Atualiza disponibilidade do prato"""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pratos SET disponivel = ? WHERE id = ?
        """, (disponivel, id_prato))
        conn.commit()
        conn.close()

    def procurar_um(self, id_prato):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pratos WHERE id=?", (id_prato,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self, id_restaurante):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pratos WHERE restaurante_id=?", (id_restaurante,))
        dados = cursor.fetchall()
        conn.close()
        return dados