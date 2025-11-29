#ver questão do status se era assim mesmo

"""
routes_entregador.py
Rotas relacionadas aos entregadores.
Inclui: área do entregador, pedidos disponíveis e minhas entregas.
"""

from flask import Blueprint, request, render_template, redirect, url_for
from ..dao.EntregadorDAO import EntregadorDAO
from ..dao.PedidoDAO import PedidoDAO

# Cria o blueprint para rotas de entregador
entregador_bp = Blueprint('entregador', __name__)

# Instancia os DAOs para acesso ao banco de dados
entregador_dao = EntregadorDAO()
pedido_dao = PedidoDAO()


# ==================== ROTA: PEDIDOS DISPONÍVEIS ====================
@entregador_bp.route("/pedidos-disponiveis/<username>", methods=['GET'])
def pedidos_disponiveis(username):
    """
    Rota para exibir todos os pedidos disponíveis para o entregador aceitar.
    
    Esta página mostra pedidos que:
    - Foram confirmados pelo restaurante
    - Ainda não têm entregador atribuído
    - Estão aguardando entrega
    
    Funcionalidades desta página:
    - Lista de pedidos disponíveis
    - Informações de cada pedido (endereço, distância, valor)
    - Botão para aceitar/recusar pedido
    - Filtros (por região, valor, etc.)
    
    Args:
        username: username do entregador logado (passado na URL)
    
    Returns:
        Renderiza o template 'pedidos_disponiveis.html' com lista de pedidos
    """
    # Verifica se o entregador existe no banco de dados
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        # Se o entregador não for encontrado, redireciona ao login
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    # Busca todos os pedidos disponíveis (sem entregador atribuído)
    # O DAO deve ter um método que filtra pedidos com status 'aguardando_entregador'
    pedidos = pedido_dao.buscar_disponiveis()
    
    # Renderiza a página com a lista de pedidos disponíveis
    # Passa tanto o entregador quanto os pedidos para o template
    return render_template('pedidos_disponiveis.html', 
                         entregador=entregador,
                         pedidos=pedidos)


# ==================== ROTA: ACEITAR PEDIDO ====================
@entregador_bp.route("/aceitar-pedido/<username>/<int:pedido_id>", methods=['POST'])
def aceitar_pedido(username, pedido_id):
    """
    Rota para processar quando um entregador aceita um pedido.
    
    Fluxo:
    1. Verifica se o pedido ainda está disponível
    2. Atribui o entregador ao pedido
    3. Atualiza status do pedido para 'em_entrega'
    4. Redireciona para "minhas entregas"
    
    Args:
        username: username do entregador
        pedido_id: ID do pedido a ser aceito
    
    Returns:
        Redirect para a página de "minhas entregas"
    """
    # Busca o entregador no banco
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return redirect(url_for('public.login'))
    
    # Atribui o pedido ao entregador
    # O DAO deve atualizar o pedido com o ID do entregador e mudar status
    sucesso = pedido_dao.atribuir_entregador(pedido_id, entregador.id)
    
    if sucesso:
        # Se conseguiu aceitar, redireciona para minhas entregas
        return redirect(url_for('entregador.minhas_entregas', username=username))
    else:
        # Se não conseguiu (pedido já foi aceito por outro), volta aos disponíveis
        return redirect(url_for('entregador.pedidos_disponiveis', 
                              username=username,
                              msg="Pedido não está mais disponível"))


# ==================== ROTA: MINHAS ENTREGAS ====================
@entregador_bp.route("/minhas-entregas/<username>", methods=['GET'])
def minhas_entregas(username):
    """
    Rota para exibir todas as entregas do entregador.
    
    Esta página mostra:
    - Entregas em andamento (status: 'em_entrega')
    - Histórico de entregas concluídas
    - Informações de cada entrega (endereço, status, horário)
    - Botões para atualizar status da entrega
    
    Funcionalidades:
    - Ver detalhes de cada entrega
    - Marcar como "coletado no restaurante"
    - Marcar como "entregue"
    - Ver histórico completo
    - Calcular ganhos
    
    Args:
        username: username do entregador logado (passado na URL)
    
    Returns:
        Renderiza o template 'minhas_entregas.html' com lista de entregas
    """
    # Verifica se o entregador existe
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    # Busca todas as entregas do entregador
    # O DAO deve filtrar pedidos onde entregador_id = entregador.id
    entregas_ativas = pedido_dao.buscar_por_entregador(entregador.id, status='em_entrega')
    entregas_concluidas = pedido_dao.buscar_por_entregador(entregador.id, status='entregue')
    
    # Renderiza a página com as entregas
    return render_template('minhas_entregas.html',
                         entregador=entregador,
                         entregas_ativas=entregas_ativas,
                         entregas_concluidas=entregas_concluidas)


# ==================== ROTA: ATUALIZAR STATUS DA ENTREGA ====================
@entregador_bp.route("/atualizar-status/<username>/<int:pedido_id>", methods=['POST'])
def atualizar_status(username, pedido_id):
    """
    Rota para atualizar o status de uma entrega.
    
    Possíveis status:
    - 'coletado': Entregador pegou o pedido no restaurante
    - 'a_caminho': Entregador está a caminho do cliente
    - 'entregue': Entrega foi concluída
    
    Args:
        username: username do entregador
        pedido_id: ID do pedido
    
    Returns:
        Redirect de volta para "minhas entregas"
    """
    # Captura o novo status enviado pelo formulário
    novo_status = request.form['status']
    
    # Atualiza o status do pedido no banco de dados
    pedido_dao.atualizar_status(pedido_id, novo_status)
    
    # Redireciona de volta para a página de minhas entregas
    return redirect(url_for('entregador.minhas_entregas', username=username))


# ==================== ROTA: ÁREA DO ENTREGADOR (DASHBOARD) ====================
@entregador_bp.route("/area/<username>", methods=['GET'])
def area_entregador(username):
    """
    Rota para o dashboard principal do entregador.
    
    Esta pode ser uma página inicial que mostra:
    - Resumo de entregas do dia
    - Ganhos do dia/semana/mês
    - Botões rápidos para "pedidos disponíveis" e "minhas entregas"
    - Estatísticas (número de entregas, avaliação média, etc.)
    
    Args:
        username: username do entregador
    
    Returns:
        Renderiza o template 'area_entregador.html'
    """
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    # Busca estatísticas do entregador
    # total_entregas = pedido_dao.contar_entregas(entregador.id)
    # ganhos_hoje = pedido_dao.calcular_ganhos(entregador.id, periodo='hoje')
    
    return render_template('area_entregador.html', entregador=entregador)


# ==================== ROTA: TRAÇAR ROTA NO MAPA ====================
@entregador_bp.route("/tracar-rota/<username>/<int:pedido_id>", methods=['GET'])
def tracar_rota(username, pedido_id):
    """
    Rota para exibir o mapa do Google Maps e traçar a rota de entrega.
    
    Funcionalidades:
    - Mostra localização atual do entregador (via GPS do navegador)
    - Mostra endereço do restaurante
    - Mostra endereço de entrega do cliente
    - Traça a melhor rota entre os três pontos
    - Calcula distância e tempo estimado
    - Permite navegação turn-by-turn
    
    Fluxo:
    1. Busca dados do entregador
    2. Busca dados do pedido (inclui restaurante e usuário)
    3. Verifica se o pedido pertence ao entregador
    4. Renderiza página com mapa e dados dos endereços
    5. JavaScript no frontend faz o traçado da rota usando Google Maps API
    
    Args:
        username: username do entregador
        pedido_id: ID do pedido para traçar rota
    
    Returns:
        Renderiza o template 'mapa_rota.html' com todos os dados necessários
    """
    # Busca o entregador no banco de dados
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    # Busca o pedido específico no banco de dados
    pedido = pedido_dao.buscar_por_id(pedido_id)
    
    if not pedido:
        return redirect(url_for('entregador.minhas_entregas', 
                              username=username,
                              msg="Pedido não encontrado!"))
    
    # Verifica se o pedido realmente pertence a este entregador
    # Isso evita que um entregador veja rotas de pedidos de outros
    if pedido.entregador_id != entregador.id:
        return redirect(url_for('entregador.minhas_entregas', 
                              username=username,
                              msg="Este pedido não pertence a você!"))
    
    # Renderiza a página com o mapa
    # Passa todos os dados necessários para o template
    return render_template('mapa_rota.html',
                         entregador=entregador,
                         pedido=pedido,
                         # Endereço do restaurante onde deve coletar o pedido
                         endereco_restaurante=pedido.restaurante.endereco,
                         nome_restaurante=pedido.restaurante.nome,
                         telefone_restaurante=pedido.restaurante.telefone,
                         # Endereço do cliente onde deve entregar
                         endereco_cliente=pedido.cliente.endereco,
                         nome_cliente=pedido.cliente.nome,
                         telefone_cliente=pedido.cliente.telefone,
                         # Informações adicionais do pedido
                         valor_pedido=pedido.valor_total,
                         status_pedido=pedido.status)


# ==================== ROTA: ATUALIZAR LOCALIZAÇÃO EM TEMPO REAL ====================
@entregador_bp.route("/atualizar-localizacao/<username>", methods=['POST'])
def atualizar_localizacao(username):
    """
    Rota API para receber e atualizar a localização do entregador em tempo real.
    
    Esta rota é chamada via JavaScript (AJAX) periodicamente enquanto o entregador
    está com o mapa aberto. Permite que o sistema saiba onde o entregador está
    e pode ser usado futuramente para rastreamento em tempo real pelo cliente.
    
    Recebe:
        - latitude: coordenada de latitude (via POST)
        - longitude: coordenada de longitude (via POST)
    
    Fluxo:
    1. Recebe coordenadas via POST
    2. Valida se o entregador existe
    3. Atualiza localização no banco de dados
    4. Retorna JSON confirmando sucesso
    
    Args:
        username: username do entregador
    
    Returns:
        JSON com status da operação
    """
    try:
        # Captura latitude e longitude enviadas pelo JavaScript
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # Valida se os dados foram enviados
        if not latitude or not longitude:
            return jsonify({
                "status": "error",
                "message": "Latitude e longitude são obrigatórias"
            }), 400
        
        # Converte para float
        lat = float(latitude)
        lng = float(longitude)
        
        # Busca o entregador
        entregador = entregador_dao.buscar_por_username(username)
        
        if not entregador:
            return jsonify({
                "status": "error",
                "message": "Entregador não encontrado"
            }), 404
        
        # Atualiza a localização no banco de dados
        # O DAO deve ter um método específico para isso
        sucesso = entregador_dao.atualizar_localizacao(entregador.id, lat, lng)
        
        if sucesso:
            return jsonify({
                "status": "success",
                "message": "Localização atualizada com sucesso",
                "latitude": lat,
                "longitude": lng
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Erro ao atualizar localização"
            }), 500
            
    except ValueError:
        # Erro se latitude/longitude não forem números válidos
        return jsonify({
            "status": "error",
            "message": "Latitude e longitude devem ser números válidos"
        }), 400
    except Exception as e:
        # Qualquer outro erro
        return jsonify({
            "status": "error",
            "message": f"Erro inesperado: {str(e)}"
        }), 500


# ==================== ROTA: INICIAR NAVEGAÇÃO ====================
@entregador_bp.route("/iniciar-navegacao/<username>/<int:pedido_id>", methods=['POST'])
def iniciar_navegacao(username, pedido_id):
    """
    Rota para registrar quando o entregador inicia a navegação.
    
    Atualiza o status do pedido e registra o horário de início da navegação.
    Útil para estatísticas e acompanhamento.
    
    Args:
        username: username do entregador
        pedido_id: ID do pedido
    
    Returns:
        Redirect de volta para a página do mapa
    """
    # Atualiza status do pedido para "em_rota" ou "saiu_para_entrega"
    pedido_dao.atualizar_status(pedido_id, 'em_rota')
    
    # Registra horário de início da navegação (se tiver campo no BD)
    # pedido_dao.registrar_inicio_navegacao(pedido_id)
    
    # Redireciona de volta para o mapa
    return redirect(url_for('entregador.tracar_rota', 
                          username=username, 
                          pedido_id=pedido_id))


# ==================== ROTAS FUTURAS (Exemplos) ====================
"""
Outras funcionalidades que podem ser adicionadas:

@entregador_bp.route("/historico/<username>", methods=['GET'])
def historico_entregas(username):
    # Histórico completo de todas as entregas com filtros
    pass

@entregador_bp.route("/ganhos/<username>", methods=['GET'])
def ver_ganhos(username):
    # Página detalhada de ganhos com gráficos e relatórios
    pass

@entregador_bp.route("/perfil/<username>", methods=['GET', 'POST'])
def atualizar_perfil(username):
    # GET: Exibe formulário de atualização
    # POST: Atualiza dados do entregador
    pass

@entregador_bp.route("/avaliacao/<username>/<int:pedido_id>", methods=['GET'])
def ver_avaliacao(username, pedido_id):
    # Ver avaliação recebida de um pedido específico
    pass
"""