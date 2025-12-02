#como ficaria a questão de representar o entregador também como o usuário? por que no código vai ter que repetir os atributos do usuário na parte do entregador

"""
routes_public.py
Rotas públicas acessíveis a qualquer visitante do site (não requerem autenticação).
Inclui: página inicial, login, escolha de tipo de cadastro e autenticação.
"""

from flask import Blueprint, request, render_template, redirect, url_for, session
from .dao.RestauranteDAO import RestauranteDAO
from .dao.UsuarioDAO import UsuarioDAO
from .dao.EntregadorDAO import EntregadorDAO

# Cria o blueprint para rotas públicas
# 'public' é o nome do blueprint
public_bp = Blueprint('public', __name__)

# Instancia os DAOs (Data Access Objects) para acesso ao banco de dados
restaurante_dao = RestauranteDAO()
usuario_dao = UsuarioDAO()
entregador_dao = EntregadorDAO()

# ==================== ROTA: FORMULÁRIO DE LOGIN ====================
@public_bp.route("/", methods=['GET'])
def login():
    """
    Rota para exibir o formulário de login.
    Usuário pode escolher entrar como:
    - Restaurante
    - Usuário
    - Entregador
    
    Returns:
        Renderiza o template 'login.html' com formulário de autenticação
    """
    return render_template('login.html')


# ==================== ROTA: PROCESSAR AUTENTICAÇÃO ====================
@public_bp.route("/autenticar", methods=['POST'])
def autenticar():
    """
    Rota para processar a autenticação (POST).
    Recebe credenciais do formulário e verifica no banco de dados.
    Redireciona para a área apropriada baseado no tipo de usuário.

    Fluxo:
    1. Recebe username, password e tipo (restaurante, usuario ou entregador) do formulário
    2. Busca no DAO correspondente
    3. Valida a senha
    4. Redireciona para a área correta ou retorna erro

    Returns:
        Redirect para área do restaurante/usuário/entregador ou volta ao login com mensagem de erro
    """
    # Captura os dados enviados pelo formulário
    username = request.form['username']
    password = request.form['password']
    tipo = request.form['tipo']  # 'restaurante', 'atendente', 'gerente' ou 'entregador'

    # Verifica qual tipo de login está sendo feito


    if tipo == 'entregador':
        # Busca entregador no banco de dados
        entregador = entregador_dao.buscar_por_username(username)

        # Verifica se o entregador existe e se a senha está correta
        if entregador and entregador['password'] == password:
            # Autenticação bem-sucedida - armazena sessão e redireciona para área do entregador
            session['entregador_username'] = username
            return redirect(url_for('entregador.area_entregador', username=username))
        else:
            # Credenciais inválidas - volta ao login com mensagem de erro
            return render_template('login.html',
                                 msg="Entregador ou senha inválidos",
                                 tipo=tipo)
    else:
        # Busca usuário no banco de dados
        usuario = usuario_dao.buscar_por_username(username)

        # Verifica se o usuário existe e se a senha está correta
        if usuario and usuario[5] == password:
            # Verifica se o usuário é um entregador - se sim, não permite login como usuário
            entregador_check = entregador_dao.buscar_por_username(username)
            if entregador_check:
                return render_template('login.html',
                                      msg="Você deve fazer login como entregador",
                                      tipo=tipo)

            # Autenticação bem-sucedida - redireciona para área do usuário
            session['user_id'] = usuario[0]
            return redirect(url_for('perfil.perfil_usuario', id_usuario=usuario[0]))

        else:
            # Credenciais inválidas - volta ao login com mensagem de erro
            return render_template('login.html',
                                  msg="Usuário ou senha inválidos",
                                  tipo=tipo)


# ==================== ROTA: LOGOUT ====================
@public_bp.route("/logout", methods=['GET'])
def logout():
    """
    Rota para fazer logout do usuário.
    Remove a sessão e redireciona para o login.
    """
    session.clear()
    return redirect(url_for('public.login'))


# ==================== ROTA: AGUARDANDO APROVAÇÃO ====================
@public_bp.route("/aguardando-aprovacao", methods=['GET'])
def aguardando_aprovacao():
    """
    Rota para exibir mensagem de aguardando aprovação.
    Acessada após cadastro de restaurante ou usuário.

    Returns:
        Renderiza o template 'aguardando_aprovacao.html' com mensagem informativa
    """
    return render_template('aguardando_aprovacao.html')


