from flask import Blueprint, request, jsonify, redirect, url_for
from .models.pedido import Pedido
from .dao.PedidoDAO import PedidoDAO
import sqlite3

pedido_bp = Blueprint("pedidos", __name__)

# Adicionar pedido
@pedido_bp.route("/pedido/novo", methods=["POST"])
def novo_pedido():
    pedido = Pedido(
        request.form['numero'],
        request.form['preco'],
        request.form['observacao'],
        request.form['pagamento'],
        request.form['status']
    )

    PedidoDAO.inserir(pedido)

    return redirect(url_for("usuario.usuario_pedidos"))


# Visualizar informações de um pedido
@pedido_bp.route("/pedido/<int:numero>", methods=["GET"])
def visualizar_pedido(numero):
    conn = sqlite3.connect("app/database/app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos WHERE numero = ?", (numero,))
    pedido = cursor.fetchone()

    conn.close()
    return jsonify(pedido), 200


# Listar apenas pedidos não concluídos
@pedido_bp.route("/pedidos/ativos", methods=["GET"])
def pedidos_ativos():
    conn = sqlite3.connect("app/database/app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos WHERE status != 'entregue'")
    pedidos = cursor.fetchall()

    conn.close()
    return jsonify(pedidos), 200


# Listar todos os pedidos
@pedido_bp.route("/listar_pedidos", methods=["GET"])
def listar_pedidos():
    conn = sqlite3.connect("app/database/app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    conn.close()
    return jsonify(pedidos), 200


# Atualizar status do pedido
@pedido_bp.route("/pedido/status/<int:numero>", methods=["POST"])
def atualizar_status(numero):

    novo_status = request.form['status']

    PedidoDAO.atualizar_status(numero, novo_status)

    return redirect(url_for('usuario.usuario_pedidos'))

