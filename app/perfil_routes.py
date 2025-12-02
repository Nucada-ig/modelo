import logging
from flask import Blueprint, render_template, session, redirect, url_for, abort, request
from .dao.UsuarioDAO import UsuarioDAO
from .dao.RestauranteDAO import RestauranteDAO

perfil_bp = Blueprint('perfil', __name__)

usuario_dao = UsuarioDAO()
restaurante_dao = RestauranteDAO()

# ROTA: PERFIL DO USUÁRIO

@perfil_bp.route("/perfil/<int:id_usuario>")
def perfil_usuario(id_usuario):
    msg = request.args.get('msg')

    #  Verifica login
    if "user_id" not in session:
        return redirect(url_for("public.login"))

    #  Garante que só pode ver o próprio perfil
    if session["user_id"] != id_usuario:
        abort(403)  # acesso proibido

    # Busca usuário no banco
    usuario = usuario_dao.buscar_por_id(id_usuario)
    if not usuario:
        abort(404)

    # usuario = (id, nome, cpf, email, telefone, username, senha, tipo, restaurante_id)
    usuario_dict = {
        "id": usuario[0],
        "nome": usuario[1],
        "cpf": usuario[2],
        "email": usuario[3],
        "telefone": usuario[4],
        "username": usuario[5],
        "senha": usuario[6],
        "tipo": usuario[7],
        "restaurante_id": usuario[8]
    }

    # Pega informações do restaurante
    restaurante_dict = None
    if usuario[8]:
        restaurante = restaurante_dao.procurar_um(usuario[8])
        if restaurante:
            restaurante_dict = {
                "id": restaurante[0],
                "nome": restaurante[1],
                "email": restaurante[4],
                "telefone": restaurante[3],
                "cnpj": restaurante[5],
                "codigo_unico": restaurante[7]
            }

    return render_template(
        "perfil_usuario.html",
        usuario=usuario_dict,
        restaurante=restaurante_dict,
        msg=msg
    )


# ROTA: DELETAR CONTA
@perfil_bp.route("/deletar_conta/<int:id_usuario>", methods=['POST'])
def deletar_conta(id_usuario):
    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("public.login"))

    # Garante que só pode deletar a própria conta
    if session["user_id"] != id_usuario:
        abort(403)

    # Verifica senha
    senha = request.form.get('senha')
    usuario = usuario_dao.buscar_por_id(id_usuario)
    if not usuario or usuario[5] != senha:
        return redirect(url_for('perfil.perfil_usuario', id_usuario=id_usuario, msg="Senha incorreta. Tente novamente."))

    # Deleta o usuário
    usuario_dao.remover(id_usuario)
    session.clear()
    return redirect(url_for("public.login"))


