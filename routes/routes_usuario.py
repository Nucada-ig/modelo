"""
routes_usuario.py
Rotas relacionadas aos usuários (clientes que fazem pedidos).
Inclui: formulário de cadastro e processamento do cadastro.
"""

from flask import Blueprint, request, render_template, redirect, url_for
from ..model.Usuario import Usuario
from ..dao.UsuarioDAO import UsuarioDAO

# Cria o blueprint para rotas de usuário
usuario_bp = Blueprint('usuario', __name__)

# Instancia o DAO para acesso ao banco de dados de usuários
usuario_dao = UsuarioDAO()


# ==================== ROTA: FORMULÁRIO DE CADASTRO ====================
@usuario_bp.route("/cadastro", methods=['GET'])
def cadastro_usuario():
    """
    Rota para exibir o formulário de cadastro de usuário.
    
    Formulário deve incluir campos como:
    - Nome completo
    - CPF
    - Email
    - Telefone
    - Endereço (para entrega) ???
    - Username (para login) ???
    - Password (para login)
    
    Returns:
        Renderiza o template 'form_cadastro_usuario.html'
    """
    return render_template('form_cadastro_usuario.html')


# ==================== ROTA: PROCESSAR CADASTRO ====================
@usuario_bp.route("/cadastrar", methods=['POST'])
def cadastrar_usuario():
    """
    Rota para processar o cadastro do usuário (POST).
    
    Fluxo:
    1. Recebe todos os dados do formulário
    2. Cria um objeto Usuario
    3. Insere no banco de dados através do DAO
    4. Redireciona para página de "aguardando aprovação"
    
    Returns:
        Redirect para a rota 'public.aguardando_aprovacao'
    """
    # Captura todos os dados enviados pelo formulário
    # request.form[] pega o valor dos inputs HTML pelo atributo 'name'
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    username = request.form['username']
    password = request.form['password']
    
    # Cria o objeto Usuario com os dados recebidos
    # Este objeto deve seguir a estrutura definida na classe Usuario do model
    usuario = Usuario(
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        endereco=endereco,
        username=username,
        password=password
    )
    
    # Insere o usuário no banco de dados
    # O DAO se encarrega de abrir conexão, executar INSERT e fechar conexão
    usuario_dao.inserir(usuario)
    
    # Redireciona para a página de aguardando aprovação
    # 'public.aguardando_aprovacao' refere-se ao blueprint 'public' e função 'aguardando_aprovacao'
    return redirect(url_for('public.aguardando_aprovacao'))


#Para discutir em conjunto:
#seria interessante colocar a outra parte de usuario junto com essa?
#ver quais das funções complementares seria interessante adicionar.