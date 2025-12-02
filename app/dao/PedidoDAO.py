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
                entregador_id INTEGER,
                preco_total REAL NOT NULL,
                forma_pagamento TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pendente',
                data TEXT,
                data_atribuicao DATETIME,
                data_entrega DATETIME,
                FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id),
                FOREIGN KEY (endereco_id) REFERENCES enderecos(id),
                FOREIGN KEY (entregador_id) REFERENCES entregadores(id)
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
        """Alias para buscar_por_id (compatibilidade com código antigo)"""
        return self.buscar_por_id(id_pedido)

    def buscar_por_id(self, id_pedido):
        """Busca um pedido específico por ID"""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE id=?", (id_pedido,))
        dado = cursor.fetchone()
        conn.close()
        return dado

    def procurar_todos(self, id_restaurante):
        """Busca todos os pedidos de um restaurante"""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos WHERE restaurante_id=?", (id_restaurante,))
        dados = cursor.fetchall()
        conn.close()
        return dados


    def buscar_disponiveis(self):
        """
        Retorna pedidos disponíveis para entregadores aceitarem.
        Critérios: sem entregador + status 'aguardando_entregador'
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, 
                   u.nome as cliente_nome, 
                   e.logradouro as endereco_entrega,
                   r.nome as restaurante_nome
            FROM pedidos p
            JOIN usuarios u ON p.cliente_id = u.id
            JOIN enderecos e ON p.endereco_id = e.id
            JOIN restaurantes r ON p.restaurante_id = r.id
            WHERE p.entregador_id IS NULL 
            AND p.status IN ('aguardando_entregador', 'confirmado')
            ORDER BY p.data ASC
        """)
        dados = cursor.fetchall()
        conn.close()
        return dados

    def atribuir_entregador(self, pedido_id, entregador_id):
        """
        Atribui um entregador a um pedido disponível.
        Retorna True se conseguiu, False se já foi atribuído.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        # Verifica se o pedido ainda está disponível
        cursor.execute("""
            SELECT entregador_id FROM pedidos WHERE id = ?
        """, (pedido_id,))
        resultado = cursor.fetchone()
        
        if not resultado or resultado[0] is not None:
            # Pedido não existe ou já tem entregador
            conn.close()
            return False
        
        # Atribui o entregador
        cursor.execute("""
            UPDATE pedidos 
            SET entregador_id = ?, 
                status = 'em_entrega',
                data_atribuicao = datetime('now')
            WHERE id = ? AND entregador_id IS NULL
        """, (entregador_id, pedido_id))
        
        conn.commit()
        sucesso = cursor.rowcount > 0
        conn.close()
        return sucesso

    def buscar_por_entregador(self, entregador_id, status=None):
        """
        Retorna pedidos de um entregador específico.
        Se status for passado, filtra por esse status.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT p.*,
                       u.nome as cliente_nome,
                       u.telefone as cliente_telefone,
                       e.logradouro as endereco_entrega,
                       e.numero as endereco_numero,
                       e.bairro as endereco_bairro,
                       r.nome as restaurante_nome,
                       r.telefone as restaurante_telefone
                FROM pedidos p
                JOIN usuarios u ON p.cliente_id = u.id
                JOIN enderecos e ON p.endereco_id = e.id
                JOIN restaurantes r ON p.restaurante_id = r.id
                WHERE p.entregador_id = ? AND p.status = ?
                ORDER BY p.data DESC
            """, (entregador_id, status))
        else:
            cursor.execute("""
                SELECT p.*,
                       u.nome as cliente_nome,
                       u.telefone as cliente_telefone,
                       e.logradouro as endereco_entrega,
                       e.numero as endereco_numero,
                       e.bairro as endereco_bairro,
                       r.nome as restaurante_nome,
                       r.telefone as restaurante_telefone
                FROM pedidos p
                JOIN usuarios u ON p.cliente_id = u.id
                JOIN enderecos e ON p.endereco_id = e.id
                JOIN restaurantes r ON p.restaurante_id = r.id
                WHERE p.entregador_id = ?
                ORDER BY p.data DESC
            """, (entregador_id,))
        
        dados = cursor.fetchall()
        conn.close()
        return dados

    def atualizar_status(self, pedido_id, novo_status):
        """
        Atualiza o status de um pedido.
        Status possíveis: 'pendente', 'confirmado', 'aguardando_entregador',
                         'em_entrega', 'coletado', 'a_caminho', 'entregue', 'cancelado'
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        # Se o status for 'entregue', registra a data de entrega
        if novo_status == 'entregue':
            cursor.execute("""
                UPDATE pedidos 
                SET status = ?, data_entrega = datetime('now')
                WHERE id = ?
            """, (novo_status, pedido_id))
        else:
            cursor.execute("""
                UPDATE pedidos 
                SET status = ?
                WHERE id = ?
            """, (novo_status, pedido_id))
        
        conn.commit()
        sucesso = cursor.rowcount > 0
        conn.close()
        return sucesso