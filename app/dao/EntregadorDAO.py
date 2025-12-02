import sqlite3

class EntregadorDAO:
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
            CREATE TABLE IF NOT EXISTS entregadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                veiculo TEXT NOT NULL,
                placa TEXT,
                status TEXT DEFAULT 'ativo',
                restaurante_id INTEGER NOT NULL,
                latitude REAL,
                longitude REAL,
                ultima_atualizacao DATETIME,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id)
            );
        """)
        conn.commit()
        conn.close()

    def inserir(self, entregador):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entregadores (usuario_id, veiculo, placa, status, restaurante_id)
            VALUES (?, ?, ?, ?, ?)
        """, (entregador.usuario_id, entregador.veiculo, entregador.placa, entregador.status, entregador.restaurante_id))
        conn.commit()
        conn.close()

    def remover(self, id_entregador):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entregadores WHERE id=?", (id_entregador,))
        conn.commit()
        conn.close()

    # ========== MÉTODO CORRIGIDO ==========
    def buscar_por_username(self, username):
        
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.usuario_id,
                e.veiculo,
                e.placa,
                e.status,
                e.latitude,
                e.longitude,
                u.nome,
                u.username,
                u.email,
                u.telefone,
                u.cpf
            FROM entregadores e
            INNER JOIN usuarios u ON e.usuario_id = u.id
            WHERE u.username = ?
        """, (username,))
        dado = cursor.fetchone()
        conn.close()
        
        # Retorna um dicionário para facilitar o acesso no template
        if dado:
            return {
                'id': dado[0],
                'usuario_id': dado[1],
                'veiculo': dado[2],
                'placa': dado[3],
                'status': dado[4],
                'latitude': dado[5],
                'longitude': dado[6],
                'nome': dado[7],
                'username': dado[8],
                'email': dado[9],
                'telefone': dado[10],
                'cpf': dado[11]
            }
        return None


    def procurar_por_username(self, username):
       
        return self.buscar_por_username(username)

    def procurar_por_id(self, id_entregador):
        """
        Busca entregador por ID com dados do usuário.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.usuario_id,
                e.veiculo,
                e.placa,
                e.status,
                e.latitude,
                e.longitude,
                u.nome,
                u.username,
                u.email,
                u.telefone,
                u.cpf
            FROM entregadores e
            INNER JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.id = ?
        """, (id_entregador,))
        dado = cursor.fetchone()
        conn.close()
        
        if dado:
            return {
                'id': dado[0],
                'usuario_id': dado[1],
                'veiculo': dado[2],
                'placa': dado[3],
                'status': dado[4],
                'latitude': dado[5],
                'longitude': dado[6],
                'nome': dado[7],
                'username': dado[8],
                'email': dado[9],
                'telefone': dado[10],
                'cpf': dado[11]
            }
        return None

    def procurar_todos(self):
        """
        Busca todos os entregadores com dados dos usuários.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.usuario_id,
                e.veiculo,
                e.placa,
                e.status,
                e.latitude,
                e.longitude,
                u.nome,
                u.username,
                u.email,
                u.telefone
            FROM entregadores e
            INNER JOIN usuarios u ON e.usuario_id = u.id
        """)
        dados = cursor.fetchall()
        conn.close()
        
        # Converte para lista de dicionários
        entregadores = []
        for dado in dados:
            entregadores.append({
                'id': dado[0],
                'usuario_id': dado[1],
                'veiculo': dado[2],
                'placa': dado[3],
                'status': dado[4],
                'latitude': dado[5],
                'longitude': dado[6],
                'nome': dado[7],
                'username': dado[8],
                'email': dado[9],
                'telefone': dado[10]
            })
        return entregadores

    def atualizar_localizacao(self, entregador_id, latitude, longitude):
        """
        Atualiza a localização GPS do entregador em tempo real.
        
        Args:
            entregador_id: ID do entregador
            latitude: Coordenada de latitude
            longitude: Coordenada de longitude
        
        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entregadores 
            SET latitude = ?, 
                longitude = ?, 
                ultima_atualizacao = datetime('now')
            WHERE id = ?
        """, (latitude, longitude, entregador_id))
        conn.commit()
        sucesso = cursor.rowcount > 0
        conn.close()
        return sucesso

    
    def atualizar_status(self, entregador_id, novo_status):
        """
        Atualiza o status do entregador.
        Status: 'ativo', 'disponível', 'em rota', 'off-line', 'voltando'
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE entregadores 
            SET status = ?
            WHERE id = ?
        """, (novo_status, entregador_id))
        conn.commit()
        sucesso = cursor.rowcount > 0
        conn.close()
        return sucesso

    def buscar_disponiveis(self):
        """
        Retorna entregadores disponíveis (status = 'disponível').
        """
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.usuario_id,
                e.veiculo,
                e.placa,
                e.status,
                e.latitude,
                e.longitude,
                u.nome,
                u.username,
                u.telefone
            FROM entregadores e
            INNER JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.status = 'disponível'
        """)
        dados = cursor.fetchall()
        conn.close()
        
        entregadores = []
        for dado in dados:
            entregadores.append({
                'id': dado[0],
                'usuario_id': dado[1],
                'veiculo': dado[2],
                'placa': dado[3],
                'status': dado[4],
                'latitude': dado[5],
                'longitude': dado[6],
                'nome': dado[7],
                'username': dado[8],
                'telefone': dado[9]
            })
        return entregadores

