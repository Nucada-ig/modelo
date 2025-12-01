import sqlite3

class PedidoDAO:
    def __init__(self, db_path='app/database/pedidos.db'):
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
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                restaurante_id INTEGER NOT NULL,
                endereco_id INTEGER NOT NULL,
                preco_total REAL NOT NULL,
                forma_pagamento TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente',
                data TEXT,
                FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id),
                FOREIGN KEY (endereco_id) REFERENCES enderecos(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, pedido):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos (cliente_id, restaurante_id, endereco_id, preco_total, forma_pagamento, status, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pedido.cliente_id, pedido.restaurante_id, pedido.endereco_id, pedido.preco_total, pedido.forma_pagamento, pedido.status, pedido.data))
        conn.commit()
        conn.close()

    def remover(self, id_pedido):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id=?", (id_pedido,))
        conn.commit()
        conn.close()

    def procurar_um(self, id_pedido):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE id=?", (id_pedido,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")
        dados = cursor.fetchall()
        conn.close()
        return dados

