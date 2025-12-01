from flask import Blueprint, request, jsonify, redirect, url_for
from models.Prato import Prato
from dao.PratoDAO import PratoDAO
import sqlite3

prato_bp = Blueprint("prato", __name__)

#prato novo
@prato_bp.route("/prato/novo", methods=["POST"])
def novo_prato():
    prato = Prato(
        request.form['valor'],
        request.form['tipo'],
        request.form['descricao'],
        request.form['id'],
        request.form['status'],
        request.form['nome']
    )

    PratoDAO.inserir(prato)

    return redirect(url_for("usuario.usuario_pratos"))



# Ver prato por ID
@prato_bp.route("/prato/<int:id>", methods=["GET"])
def ver_prato(id):
    conn = sqlite3.connect("pratos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pratos WHERE id = ?", (id,))
    prato = cursor.fetchone()
    conn.close()
    return jsonify(prato), 200


# Listar pratos ativos
#@prato_bp.route("/pratos/ativos", methods=["GET"])
########## tem que listar todos os pratos, não só os ativos para poderem ser editados depois
#def pratos_ativos():
   # conn = sqlite3.connect("pratos.db")
    #cursor = conn.cursor()
    #cursor.execute("SELECT * FROM pratos WHERE status = 'ativo'")
    #pratos = cursor.fetchall()
    #conn.close()
    #return jsonify(pratos), 200


# Alterar status
@prato_bp.route("/prato/status/<int:id>", methods=["POST"])
def alterar_status(id):
    status = request.form['status']

    PratoDAO.atualizar_status(id, status)

    return redirect(url_for("usuario.usuario_pratos"))



# Remover prato
@prato_bp.route("/prato/remover/<int:id>", methods=["POST"])
def remover_prato(id):
    PratoDAO.remover(id)
    return redirect(url_for("usuario.usuario_pratos"))

