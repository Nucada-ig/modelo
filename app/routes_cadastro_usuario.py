"""
routes_usuario.py
Rotas relacionadas aos usuários (clientes que fazem pedidos).
Inclui: formulário de cadastro e processamento do cadastro.
"""

from flask import Blueprint, request, render_template, redirect, url_for
from app.models.usuario import Usuario_class as Usuario
from app.models.entregador import Entregador
from .dao.UsuarioDAO import UsuarioDAO
from .dao.EntregadorDAO import EntregadorDAO
from .dao.RestauranteDAO import RestauranteDAO

# Cria o blueprint para rotas de usuário
usuario_bp = Blueprint('usuario', __name__)

# Instancia o DAO para acesso ao banco de dados de usuários
usuario_dao = UsuarioDAO()
entregador_dao = EntregadorDAO()
restaurante_dao = RestauranteDAO()


# ==================== ROTA: FORMULÁRIO DE CADASTRO ====================
@usuario_bp.route("/cadastro_usuario", methods=['GET'])
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
@usuario_bp.route("/cadastrar_usuario", methods=['POST'])
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
    username = request.form['username']
    password = request.form['password']
    tipo = request.form['tipo']
    codigo_restaurante = request.form['codigo_unico']  

    restaurante = restaurante_dao.procurar_por_codigo(codigo_restaurante)
    if restaurante is None:
        # Código do restaurante inválido
        return render_template('form_cadastro_usuario.html', msg="Código do restaurante inválido. Verifique e tente novamente.")

    # Verifica se o username já existe
    if usuario_dao.username_existe(username):
        return render_template('form_cadastro_usuario.html', msg="Username já existe. Escolha outro username.")

    # Cria o objeto Usuario com os dados recebidos
    # Este objeto deve seguir a estrutura definida na classe Usuario do model
    if tipo == 'entregador':
        # Criar usuário primeiro
        usuario_entregador = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            username=username,
            senha=password,
            tipo='entregador',
            restaurante_id=restaurante[0]
        )
        usuario_id = usuario_dao.inserir(usuario_entregador)

        # Criar entregador
        entregador = Entregador(
            usuario_id=usuario_id,
            nome=nome,
            email=email,
            senha=password,
            CPF=cpf,
            telefone=telefone,
            tipo='entregador',
            veiculo='Não informado',
            placa=None,
            status='inativo',
            restaurante_id=restaurante[0]
        )

        entregador_dao.inserir(entregador)
    else:
        usuario = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            username=username,
            senha=password,
            tipo= tipo,
            restaurante_id= restaurante[0]  # Pega o id do restaurante (primeiro campo da tupla)
        )
        usuario_dao.inserir(usuario)

    # Redireciona para a página de aguardando aprovação
    # 'public.aguardando_aprovacao' refere-se ao blueprint 'public' e função 'aguardando_aprovacao'
    return redirect(url_for('public.aguardando_aprovacao'))

