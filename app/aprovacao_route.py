from flask import Blueprint, request, jsonify, redirect, url_for
from dao.AplicantesDAO import AplicanteDAO
import sqlite3

aprovacao_bp = Blueprint("aprovacao", __name__)

# Ver aplicantes
@aprovacao_bp.route("/aplicantes", methods=["GET"])
def listar_aplicantes():
    conn = sqlite3.connect("aplicantes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aplicantes")
    lista = cursor.fetchall()
    conn.close()
    return jsonify(lista), 200


# Aprovar aplicante
@aprovacao_bp.route("/aplicante/aprovar/<int:id>", methods=["POST"])
def aprovar(id):

    tipo_destino = request.form['tipo']  # entregador, atendente, gerente

    aplicante = AplicanteDAO.buscar(id)

    AplicanteDAO.aprovar(aplicante, tipo_destino)

    return redirect(url_for("usuario.usuario_aprovacao"))



# Recusar aplicante
@aprovacao_bp.route("/aplicante/recusar/<int:id>", methods=["POST"])
def recusar(id):

    justificativa = request.form.get('motivo', '')  # se quiser usar

    AplicanteDAO.remover(id)

    return redirect(url_for("usuario.usuario_aprovacao"))
