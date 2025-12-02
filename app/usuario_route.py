import sqlite3
import sqlite3
from flask import Blueprint, render_template, session
from .dao.UsuarioDAO import UsuarioDAO
from .dao.PedidoDAO import PedidoDAO
from .dao.RestauranteDAO import RestauranteDAO
from .dao.EnderecoDAO import EnderecoDAO
from .dao.PratoDAO import PratoDAO
from .dao.EntregadorDAO import EntregadorDAO

usuario_bp = Blueprint("usuario", __name__)

# Página principal do usuário — acessa todos os menus
@usuario_bp.route("/dashboard", methods=["GET"])
def usuario_home():
    return render_template("dashboard.html")

# Cada página simples
@usuario_bp.route("/pedidos", methods=["GET"])
def usuario_pedidos():
    return render_template("pedidos.html")

@usuario_bp.route("/pratos", methods=["GET"])
def usuario_pratos():
    return render_template("pratos.html")

@usuario_bp.route("/entregadores", methods=["GET"])
def usuario_entregadores():
    return render_template("entregadores.html")

@usuario_bp.route("/aprovacao/<int:id>", methods=["GET"])
def usuario_aprovacao(id):
    print(f"Accessing approval panel for user id: {id}")
    return render_template("aprovacao.html")

@usuario_bp.route("/pedidos_restaurante/<int:id>", methods=["GET"])
def usuario_pedidos_restaurante(id):
    # Verificar se o usuário existe
    usuario_dao = UsuarioDAO()
    usuario_tuple = usuario_dao.buscar_por_id(id)
    if not usuario_tuple:
        return render_template("login.html"), 404

    # Converter para dict
    usuario = {
        "id": usuario_tuple[0],
        "nome": usuario_tuple[1],
        "cpf": usuario_tuple[2],
        "email": usuario_tuple[3],
        "telefone": usuario_tuple[4],
        "username": usuario_tuple[5],
        "tipo": usuario_tuple[6],
        "restaurante_id": usuario_tuple[8]
    }

    # Obter o restaurante associado ao usuário
    restaurante_id = usuario_tuple[8]
    restaurante = None
    if restaurante_id:
        restaurante_dao = RestauranteDAO()
        restaurante_tuple = restaurante_dao.procurar_um(restaurante_id)
        if restaurante_tuple:
            restaurante = {
                "id": restaurante_tuple[0],
                "nome": restaurante_tuple[1],
                "email": restaurante_tuple[4],
                "telefone": restaurante_tuple[3],
                "cnpj": restaurante_tuple[5],
                "codigo_unico": restaurante_tuple[7]
            }

    # Obter os pedidos do restaurante
    pedidos_raw = []
    if restaurante_id:
        pedido_dao = PedidoDAO()
        pedidos_raw = pedido_dao.procurar_todos(restaurante_id)

    # Para cada pedido, as informações do cliente e endereço já estão na tupla
    pedidos = []
    prato_dao = PratoDAO()
    for p in pedidos_raw:
        cliente_nome = p[1]  # cliente_nome
        endereco_str = p[3]  # endereco
        # Buscar nomes dos pratos
        pratos_nomes = []
        if p[11]:  # pratos_ids
            ids = [int(id.strip()) for id in p[11].split(',') if id.strip()]
            for id_prato in ids:
                prato = prato_dao.procurar_um(id_prato)
                if prato:
                    pratos_nomes.append(prato[2])  # nome is index 2
        pratos_str = ', '.join(pratos_nomes) if pratos_nomes else 'Nenhum prato selecionado'
        # Adicionar as informações ao pedido
        pedidos.append(p + (cliente_nome, endereco_str, pratos_str))

    return render_template("pedidos_restaurante.html", usuario=usuario, restaurante=restaurante, pedidos=pedidos)

@usuario_bp.route("/pratos_restaurante/<int:id>", methods=["GET"])
def usuario_pratos_restaurante(id):
    # Verificar se o usuário existe
    usuario_dao = UsuarioDAO()
    usuario_tuple = usuario_dao.buscar_por_id(id)
    if not usuario_tuple:
        return render_template("login.html"), 404

    # Converter para dict
    usuario = {
        "id": usuario_tuple[0],
        "nome": usuario_tuple[1],
        "cpf": usuario_tuple[2],
        "email": usuario_tuple[3],
        "telefone": usuario_tuple[4],
        "username": usuario_tuple[5],
        "tipo": usuario_tuple[6],
        "restaurante_id": usuario_tuple[8]
    }

    # Obter o restaurante associado ao usuário
    restaurante_id = usuario_tuple[8]
    restaurante = None
    if restaurante_id:
        restaurante_dao = RestauranteDAO()
        restaurante_tuple = restaurante_dao.procurar_um(restaurante_id)
        if restaurante_tuple:
            restaurante = {
                "id": restaurante_tuple[0],
                "nome": restaurante_tuple[1],
                "email": restaurante_tuple[4],
                "telefone": restaurante_tuple[3],
                "cnpj": restaurante_tuple[5],
                "codigo_unico": restaurante_tuple[7]
            }

    # Obter os pratos do restaurante
    pratos = []
    if restaurante_id:
        prato_dao = PratoDAO()
        pratos = prato_dao.procurar_todos(restaurante_id)

    return render_template("pratos_restaurante.html", usuario=usuario, restaurante=restaurante, pratos=pratos)

@usuario_bp.route("/entregadores_restaurante/<int:id>", methods=["GET"])
def usuario_entregadores_restaurante(id):
    # Verificar se o usuário existe
    usuario_dao = UsuarioDAO()
    usuario_tuple = usuario_dao.buscar_por_id(id)
    if not usuario_tuple:
        return render_template("login.html"), 404

    # Converter para dict
    usuario = {
        "id": usuario_tuple[0],
        "nome": usuario_tuple[1],
        "cpf": usuario_tuple[2],
        "email": usuario_tuple[3],
        "telefone": usuario_tuple[4],
        "username": usuario_tuple[5],
        "tipo": usuario_tuple[6],
        "restaurante_id": usuario_tuple[8]
    }

    # Obter o restaurante associado ao usuário
    restaurante_id = usuario_tuple[8]
    restaurante = None
    if restaurante_id:
        restaurante_dao = RestauranteDAO()
        restaurante_tuple = restaurante_dao.procurar_um(restaurante_id)
        if restaurante_tuple:
            restaurante = {
                "id": restaurante_tuple[0],
                "nome": restaurante_tuple[1],
                "email": restaurante_tuple[4],
                "telefone": restaurante_tuple[3],
                "cnpj": restaurante_tuple[5],
                "codigo_unico": restaurante_tuple[7]
            }

    # Obter os entregadores do restaurante
    entregadores = []
    if restaurante_id:
        entregador_dao = EntregadorDAO()
        entregadores = entregador_dao.procurar_todos_por_restaurante(restaurante_id)

    return render_template("entregadores_restaurante.html", usuario=usuario, restaurante=restaurante, entregadores=entregadores)

@usuario_bp.route("/atualizar_status_pedido/<int:id>/<int:pedido_id>", methods=["POST"])
def atualizar_status_pedido(id, pedido_id):
    from flask import request, redirect, url_for

    # Verificar usuário
    usuario_dao = UsuarioDAO()
    usuario_tuple = usuario_dao.buscar_por_id(id)
    if not usuario_tuple:
        return "User not found", 404

    novo_status = request.form['status']

    # Atualizar status do pedido
    pedido_dao = PedidoDAO()
    pedido_dao.atualizar_status(pedido_id, novo_status)

    return redirect(url_for('usuario.usuario_pedidos_restaurante', id=id))

@usuario_bp.route("/novo_pedido_restaurante/<int:id>", methods=["POST"])
def novo_pedido_restaurante(id):
    from flask import request, redirect, url_for
    from datetime import datetime

    # Verificar usuário
    usuario_dao = UsuarioDAO()
    usuario_tuple = usuario_dao.buscar_por_id(id)
    print(f"Usuario tuple: {usuario_tuple}")
    if not usuario_tuple:
        return "User not found", 404

    restaurante_id = usuario_tuple[8]
    print(f"Restaurante ID: {restaurante_id}")

    nome_cliente = request.form['nome_cliente']
    endereco_str = request.form['endereco']
    preco_total = float(request.form['preco_total'])
    forma_pagamento = request.form['forma_pagamento']
    pratos_ids_str = request.form.get('pratos_ids', '')
    print(f"DEBUG: pratos_ids_str = '{pratos_ids_str}'")

    # Pratos IDs (não usado na inserção, mas aceito)
    pratos_ids = [int(pid.strip()) for pid in pratos_ids_str.split(',') if pid.strip()]

    status = 'pendente'
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Criar objeto temporário para inserção
    class PedidoTemp:
        def __init__(self, cliente_nome, restaurante_id, endereco, preco_total, forma_pagamento, status, data, pratos_ids):
            self.cliente_nome = cliente_nome
            self.restaurante_id = restaurante_id
            self.endereco = endereco
            self.preco_total = preco_total
            self.forma_pagamento = forma_pagamento
            self.status = status
            self.data = data
            self.pratos_ids = pratos_ids

    pedido = PedidoTemp(nome_cliente, restaurante_id, endereco_str, preco_total, forma_pagamento, status, data, pratos_ids_str)

    pedido_dao = PedidoDAO()
    pedido_dao.inserir(pedido)

    return redirect(url_for('usuario.usuario_pedidos_restaurante', id=id))

@usuario_bp.route("/novo_prato_restaurante/<int:id>", methods=["POST"])
def novo_prato_restaurante(id):
    from flask import request, redirect, url_for

    try:
        # Verificar usuário
        usuario_dao = UsuarioDAO()
        usuario_tuple = usuario_dao.buscar_por_id(id)
        if not usuario_tuple:
            return "User not found", 404

        restaurante_id = usuario_tuple[8]

        nome = request.form['nome']
        descricao = request.form.get('descricao', '')
        preco = float(request.form['preco'])
        tempo_preparo = request.form.get('tempo_preparo')
        tempo_preparo = int(tempo_preparo) if tempo_preparo else None
        disponivel = 1
        destaque = 0

        from .models.prato import Prato
        prato = Prato(
            restaurante_id=restaurante_id,
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria='',
            disponivel=disponivel,
            tempo_preparo=tempo_preparo,
            destaque=destaque
        )

        prato_dao = PratoDAO()
        prato_dao.inserir(prato)

        return redirect(url_for('usuario.usuario_pratos_restaurante', id=id))
    except Exception as e:
        return f"Error: {e}", 500

@usuario_bp.route("/config", methods=["GET"])
def usuario_config():
    return render_template("config.html")
