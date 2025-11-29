"""
routes_restaurante.py
Rotas relacionadas aos restaurantes.
Inclui: formulário de cadastro, processamento do cadastro e área do restaurante.
"""

from flask import Blueprint, request, render_template, redirect, url_for
from ..model.Restaurante import Restaurante
from ..dao.RestauranteDAO import RestauranteDAO

# Cria o blueprint para rotas de restaurante
restaurante_bp = Blueprint('restaurante', __name__)

# Instancia o DAO para acesso ao banco de dados de restaurantes
restaurante_dao = RestauranteDAO()


# ==================== ROTA: FORMULÁRIO DE CADASTRO ====================
@restaurante_bp.route("/cadastro", methods=['GET'])
def cadastro_restaurante():
    """
    Rota para exibir o formulário de cadastro de restaurante.
    
    Formulário deve incluir campos como:
    - Nome do restaurante
    - CNPJ
    - Endereço
    - Telefone
    - Email
    - Username (para login)
    - Password (para login)
    
    Returns:
        Renderiza o template 'form_cadastro_restaurante.html'
    """
    return render_template('form_cadastro_restaurante.html')


# ==================== ROTA: PROCESSAR CADASTRO ====================
@restaurante_bp.route("/cadastrar", methods=['POST'])
def cadastrar_restaurante():
    """
    Rota para processar o cadastro do restaurante (POST).
    
    Fluxo:
    1. Recebe todos os dados do formulário
    2. Cria um objeto Restaurante
    3. Insere no banco de dados através do DAO
    4. Redireciona para página de "aguardando aprovação"
    
    Returns:
        Redirect para a rota 'public.aguardando_aprovacao'
    """
    # Captura todos os dados enviados pelo formulário
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    # Cria o objeto Restaurante com os dados recebidos
    # Este objeto deve seguir a estrutura definida na classe Restaurante do model!!!
    restaurante = Restaurante(
        nome=nome,
        cnpj=cnpj,
        endereco=endereco,
        telefone=telefone,
        email=email,
        username=username,
        password=password,
    )
    
    # Insere o restaurante no banco de dados
    # O DAO se encarrega de abrir conexão, executar INSERT e fechar conexão
    restaurante_dao.inserir(restaurante)
    
    # Redireciona para a página de aguardando aprovação
    # 'public.aguardando_aprovacao' refere-se ao blueprint 'public' e função 'aguardando_aprovacao'
    return redirect(url_for('public.aguardando_aprovacao'))


# ==================== ROTA: ÁREA DO RESTAURANTE ====================
#Essa área é necessária?
@restaurante_bp.route("/area/<username>", methods=['GET'])
def area_restaurante(username):
    """
    Rota para a área logada do restaurante.
    Exibe informações e opções específicas do restaurante.
    
    Esta área pode incluir:
    - Informações do restaurante
    - Gerenciar cardápio
    - Ver pedidos recebidos
    - Estatísticas
    
    Args:
        username: username do restaurante (passado na URL)
    
    Returns:
        Renderiza o template 'area_restaurante.html' com dados do restaurante
        ou redireciona ao login se restaurante não for encontrado
    """
    # Busca o restaurante no banco de dados pelo username
    restaurante = restaurante_dao.buscar_por_username(username)
    
    # Verifica se o restaurante foi encontrado
    if not restaurante:
        # Se não encontrou, redireciona ao login com mensagem de erro
        return render_template('login.html', 
                             msg="Restaurante não encontrado!",
                             tipo='restaurante')
    
    # Se encontrou, renderiza a página da área do restaurante
    # Passa o objeto restaurante para o template poder exibir os dados
    return render_template('area_restaurante.html', restaurante=restaurante)


# ==================== ROTAS FUTURAS (Exemplos) ====================
"""
@restaurante_bp.route("/atualizar/<username>", methods=['GET'])
def form_atualizar_restaurante(username):
    # Exibe formulário para atualizar dados do restaurante
    pass

@restaurante_bp.route("/atualizar", methods=['POST'])
def atualizar_restaurante():
    # Processa atualização dos dados do restaurante
    pass

@restaurante_bp.route("/cardapio/<username>", methods=['GET'])
def gerenciar_cardapio(username):
    # Página para gerenciar itens do cardápio
    pass

@restaurante_bp.route("/pedidos/<username>", methods=['GET'])
def ver_pedidos(username):
    # Página para visualizar pedidos recebidos
    pass
"""
