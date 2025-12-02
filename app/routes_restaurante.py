"""
routes_restaurante.py
Rotas relacionadas aos restaurantes.
Inclui: formulário de cadastro, processamento do cadastro e área do restaurante.
"""

import logging
from flask import Blueprint, request, render_template, redirect, url_for
from app.models.restaurante import Restaurante
from .dao.RestauranteDAO import RestauranteDAO
from .dao.UsuarioDAO import UsuarioDAO
from app.models.usuario import Usuario_class as Usuario

# Cria o blueprint para rotas de restaurante
restaurante_bp = Blueprint('restaurante', __name__, url_prefix='/restaurante')

# Instancia o DAO para acesso ao banco de dados de restaurantes
restaurante_dao = RestauranteDAO()
usuario_dao = UsuarioDAO()


# ==================== ROTA: FORMULÁRIO DE CADASTRO ====================
@restaurante_bp.route("/cadastro", methods=['GET'])
def cadastro_restaurante():
    """
    Rota para exibir o formulário de cadastro de restaurante.
    """
    return render_template('form_cadastro_restaurante.html')


# ==================== ROTA: PROCESSAR CADASTRO ====================
@restaurante_bp.route("/cadastrar_restaurante", methods=['POST'])
def cadastrar_restaurante():
    """
    Rota para processar o cadastro do restaurante (POST).

    Fluxo:
    1. Recebe dados do formulário (incluindo dados do responsável).
    2. Cria e Insere o objeto Usuario (Responsável do Restaurante, tipo='restaurante').
    3. Cria e Insere o objeto Restaurante.
    4. Redireciona para página de "aguardando aprovação".

    Returns:
        Redirect para a rota 'public.aguardando_aprovacao'
    """
    # 1. Captura todos os dados enviados pelo formulário
    # Dados do Usuário (Responsável)
    nome_user = request.form['nome_responsavel'] # Alterei o nome da variável para maior clareza
    cpf_user = request.form['cpf']
    email_user = request.form['email_responsavel']
    telefone_user = request.form['telefone_responsavel']
    username_user = request.form['username']
    password_user = request.form['password']

    # Dados do Restaurante
    nome_restaurante = request.form['nome_restaurante'] # Variável ajustada
    cnpj = request.form['cnpj']
    endereco = request.form['endereco']
    telefone_restaurante = request.form['telefone_restaurante'] # Variável ajustada
    email_restaurante = request.form['email_restaurante']
    codigo_unico = request.form.get('codigo_unico')  # Opcional

    restaurante = Restaurante(
        nome=nome_restaurante,
        endereco=endereco,
        telefone=telefone_restaurante,
        CNPJ=cnpj,
        email=email_restaurante,
        nome_responsavel=nome_user, # Usa o nome do responsável recém-cadastrado
        codigo_unico=codigo_unico if codigo_unico else None
    )
    try:
        restaurante_id = restaurante_dao.inserir(restaurante)
    except Exception as e:
        logging.error(f"Failed to insert restaurant: {e}")
        # If restaurant insertion fails, don't create the user
        return redirect(url_for('public.aguardando_aprovacao'))  # Or show error, but for now redirect

    usuario = Usuario(
        nome=nome_user,
        cpf=cpf_user,
        email=email_user,
        telefone=telefone_user,
        username=username_user,
        senha=password_user,
        tipo='restaurante',
        restaurante_id= restaurante_id
    )
    usuario_dao.inserir(usuario)
    return redirect(url_for('public.aguardando_aprovacao'))



