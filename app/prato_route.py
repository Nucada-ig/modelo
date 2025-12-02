from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from .models.prato import Prato
from .dao.PratoDAO import PratoDAO
from werkzeug.utils import secure_filename
import os
import sqlite3

prato_bp = Blueprint("prato", __name__)
prato_dao = PratoDAO()

# Configuração de upload de imagens
UPLOAD_FOLDER = 'static/uploads/pratos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@prato_bp.route("/prato/novo", methods=["POST"])
def novo_prato():
    """Cria um novo prato"""
    try:
        # Processar imagem se foi enviada
        imagem_filename = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Adicionar timestamp para evitar conflitos
                import time
                imagem_filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(UPLOAD_FOLDER, imagem_filename))
        
        # Criar objeto Prato
        prato = Prato(
            restaurante_id=int(request.form['restaurante_id']),
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            preco=float(request.form['preco']),
            categoria=request.form['categoria'],
            disponivel=1 if request.form.get('disponivel') == '1' else 0,
            tempo_preparo=int(request.form['tempo_preparo']) if request.form.get('tempo_preparo') else None,
            destaque=1 if request.form.get('destaque') == '1' else 0,
            imagem=imagem_filename
        )

        prato_dao.inserir(prato)

        return redirect(url_for("restaurante.cardapio", username=request.form.get('username', 'default')))
    
    except Exception as e:
        print(f"Erro ao criar prato: {e}")
        return jsonify({'error': str(e)}), 400


@prato_bp.route("/prato/<int:id>", methods=["GET"])
def ver_prato(id):
    """Retorna dados de um prato específico em JSON"""
    prato = prato_dao.procurar_um(id)
    if prato:
        return jsonify({
            'id': prato[0],
            'restaurante_id': prato[1],
            'nome': prato[2],
            'descricao': prato[3],
            'preco': prato[4],
            'categoria': prato[5],
            'disponivel': prato[6],
            'tempo_preparo': prato[7],
            'destaque': prato[8],
            'imagem': prato[9]
        }), 200
    return jsonify({'error': 'Prato não encontrado'}), 404


# Listar todos os pratos
@prato_bp.route("/listar_pratos", methods=["GET"])
def listar_pratos():
    conn = sqlite3.connect("app/database/pedidos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pratos")
    pratos = cursor.fetchall()
    conn.close()
    return jsonify(pratos), 200


# Alterar status
@prato_bp.route("/prato/status/<int:id>", methods=["POST"])
def alterar_status(id):
    """Altera a disponibilidade do prato"""
    disponivel = int(request.form.get('disponivel', 0))
    prato_dao.atualizar_status(id, disponivel)
    return redirect(url_for("restaurante.cardapio", username=request.form.get('username', 'default')))


@prato_bp.route("/prato/remover/<int:id>", methods=["POST"])
def remover_prato(id):
    """Remove um prato"""
    prato_dao.remover(id)
    return redirect(url_for("restaurante.cardapio", username=request.form.get('username', 'default')))