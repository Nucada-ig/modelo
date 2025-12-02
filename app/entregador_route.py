"""
routes_entregador.py
Rotas relacionadas aos entregadores.
"""

from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, abort
from app.dao.EntregadorDAO import EntregadorDAO
from app.dao.PedidoDAO import PedidoDAO
from app.dao.UsuarioDAO import UsuarioDAO
from app.dao.RestauranteDAO import RestauranteDAO
import sqlite3

# Cria o blueprint
entregador_bp = Blueprint('entregador', __name__)

# Instancia os DAOs
entregador_dao = EntregadorDAO()
pedido_dao = PedidoDAO()
usuario_dao = UsuarioDAO()
restaurante_dao = RestauranteDAO()


@entregador_bp.route("/api/entregador/<int:id>", methods=["GET"])
def ver_entregador_api(id):
    """
    API: Retorna dados de um entregador específico em JSON.
    Útil para dashboards administrativos ou integrações.
    """
    entregador = entregador_dao.procurar_por_id(id)
    if entregador:
        return jsonify(entregador), 200
    return jsonify({"error": "Entregador não encontrado"}), 404


@entregador_bp.route("/api/entregadores", methods=["GET"])
def listar_entregadores_api():
    """
    API: Lista todos os entregadores em JSON.
    Útil para dashboards administrativos ou relatórios.
    """
    entregadores = entregador_dao.procurar_todos()
    return jsonify(entregadores), 200


@entregador_bp.route("/pedidos-disponiveis/<username>", methods=['GET'])
def pedidos_disponiveis(username):
    """Página com pedidos disponíveis para o entregador aceitar"""
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    pedidos = pedido_dao.buscar_disponiveis()
    
    return render_template('pedidos_disponiveis.html', 
                         entregador=entregador,
                         pedidos=pedidos)


@entregador_bp.route("/aceitar-pedido/<username>/<int:pedido_id>", methods=['POST'])
def aceitar_pedido(username, pedido_id):
    """Processa quando um entregador aceita um pedido"""
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return redirect(url_for('public.login'))
    
    sucesso = pedido_dao.atribuir_entregador(pedido_id, entregador['id'])

    if sucesso:
        return redirect(url_for('entregador.area_entregador', username=username, msg="Pedido aceito com sucesso", tab="minhas"))
    else:
        return redirect(url_for('entregador.area_entregador',
                              username=username,
                              msg="Pedido não está mais disponível"))


@entregador_bp.route("/minhas-entregas/<username>", methods=['GET'])
def minhas_entregas(username):
    """Página com entregas ativas e concluídas do entregador"""
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    entregas_ativas = pedido_dao.buscar_por_entregador(entregador['id'], status='com_entregador')
    pedidos_disponiveis = pedido_dao.buscar_disponiveis()
    
    return render_template('dashboard.html',
                         entregador=entregador,
                         entregas_ativas=entregas_ativas,
                         pedidos_disponiveis=pedidos_disponiveis)


@entregador_bp.route("/atualizar-status/<username>/<int:pedido_id>", methods=['POST'])
def atualizar_status(username, pedido_id):
    """Atualiza o status de uma entrega"""
    novo_status = request.form['status']
    pedido_dao.atualizar_status(pedido_id, novo_status)
    return redirect(url_for('entregador.minhas_entregas', username=username))


@entregador_bp.route("/area/<username>", methods=['GET'])
def area_entregador(username):
    """Dashboard principal do entregador"""
    msg = request.args.get('msg')
    entregador = entregador_dao.buscar_por_username(username)

    if not entregador:
        return render_template('login.html',
                              msg="Entregador não encontrado!",
                              tipo='entregador')

    pedidos_disponiveis = pedido_dao.buscar_disponiveis()
    entregas_ativas = pedido_dao.buscar_por_entregador(entregador['id'], status='com_entregador')

    return render_template('area_entregador.html',
                           entregador=entregador,
                           pedidos_disponiveis=pedidos_disponiveis,
                           entregas_ativas=entregas_ativas,
                           msg=msg)


@entregador_bp.route("/tracar-rota/<username>/<int:pedido_id>", methods=['GET'])
def tracar_rota(username, pedido_id):
    """Exibe o mapa com a rota de entrega"""
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    pedido = pedido_dao.buscar_por_id(pedido_id)
    
    if not pedido:
        return redirect(url_for('entregador.minhas_entregas', 
                              username=username,
                              msg="Pedido não encontrado!"))
    
    # Verifica se o pedido pertence a este entregador
    if pedido['entregador_id'] != entregador['id']:
        return redirect(url_for('entregador.minhas_entregas', 
                              username=username,
                              msg="Este pedido não pertence a você!"))
    
    return render_template('entrega_atual.html',
                         entregador=entregador,
                         pedido=pedido)


@entregador_bp.route("/atualizar-localizacao/<username>", methods=['POST'])
def atualizar_localizacao(username):
    """API: Atualiza localização GPS do entregador em tempo real"""
    try:
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if not latitude or not longitude:
            return jsonify({
                "status": "error",
                "message": "Latitude e longitude são obrigatórias"
            }), 400
        
        lat = float(latitude)
        lng = float(longitude)
        
        entregador = entregador_dao.buscar_por_username(username)
        
        if not entregador:
            return jsonify({
                "status": "error",
                "message": "Entregador não encontrado"
            }), 404
        
        sucesso = entregador_dao.atualizar_localizacao(entregador['id'], lat, lng)
        
        if sucesso:
            return jsonify({
                "status": "success",
                "message": "Localização atualizada com sucesso",
                "latitude": lat,
                "longitude": lng
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Erro ao atualizar localização"
            }), 500
            
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Latitude e longitude devem ser números válidos"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro inesperado: {str(e)}"
        }), 500


@entregador_bp.route("/iniciar-navegacao/<username>/<int:pedido_id>", methods=['POST'])
def iniciar_navegacao(username, pedido_id):
    """Registra quando o entregador inicia a navegação"""
    pedido_dao.atualizar_status(pedido_id, 'em_rota')
    return redirect(url_for('entregador.tracar_rota', 
                          username=username, 
                          pedido_id=pedido_id))


@entregador_bp.route("/historico/<username>", methods=['GET'])
def historico_entregas(username):
    """Exibe histórico de entregas com filtros"""
    entregador = entregador_dao.buscar_por_username(username)
    
    if not entregador:
        return render_template('login.html', 
                             msg="Entregador não encontrado!",
                             tipo='entregador')
    
    periodo = request.args.get('periodo', 'hoje')
    
    entregas_concluidas = pedido_dao.buscar_por_entregador(entregador['id'], status='entregue')
    
    # Calcular estatísticas
    stats = {
        'entregas_hoje': pedido_dao.contar_entregas(entregador['id'], periodo='hoje'),
        'ganhos_hoje': pedido_dao.calcular_ganhos(entregador['id'], periodo='hoje'),
        'entregas_semana': pedido_dao.contar_entregas(entregador['id'], periodo='semana'),
        'ganhos_semana': pedido_dao.calcular_ganhos(entregador['id'], periodo='semana'),
        'entregas_mes': pedido_dao.contar_entregas(entregador['id'], periodo='mes'),
        'ganhos_mes': pedido_dao.calcular_ganhos(entregador['id'], periodo='mes'),
    }
    
    return render_template('historico.html',
                         entregador=entregador,
                         entregas_concluidas=entregas_concluidas[:20],
                         tem_mais_entregas=len(entregas_concluidas) > 20,
                         periodo=periodo,
                         stats=stats)


@entregador_bp.route("/deletar_conta/<username>", methods=['POST'])
def deletar_conta_entregador(username):
    # Verifica se está logado como entregador
    if "entregador_username" not in session or session["entregador_username"] != username:
        abort(403)

    # Busca o entregador
    entregador = entregador_dao.buscar_por_username(username)
    if not entregador:
        abort(404)

    # Verifica senha
    senha = request.form.get('senha')
    if entregador['password'] != senha:
        return redirect(url_for('entregador.area_entregador', username=username, msg="Senha incorreta. Tente novamente."))

    # Deleta o entregador da tabela entregadores
    entregador_dao.remover(entregador['id'])

    # Deleta o usuário da tabela usuarios
    usuario_dao.remover(entregador['usuario_id'])

    session.clear()
    return redirect(url_for("public.login"))


@entregador_bp.route("/perfil/<username>", methods=['GET'])
def perfil_entregador(username):
    # Verifica se está logado como entregador
    if "entregador_username" not in session or session["entregador_username"] != username:
        abort(403)

    # Busca o entregador
    entregador = entregador_dao.buscar_por_username(username)
    if not entregador:
        abort(404)

    # Busca informações do restaurante
    restaurante_dict = None
    if entregador.get('restaurante_id'):
        restaurante = restaurante_dao.procurar_um(entregador['restaurante_id'])
        if restaurante:
            restaurante_dict = {
                "id": restaurante[0],
                "nome": restaurante[1],
                "email": restaurante[4],
                "telefone": restaurante[3],
                "cnpj": restaurante[5],
                "codigo_unico": restaurante[7]
            }

    return render_template('perfil_entregador.html', entregador=entregador, restaurante=restaurante_dict)


@entregador_bp.route("/atualizar_status/<username>", methods=['POST'])
def atualizar_status_entregador(username):
    # Verifica se está logado como entregador
    if "entregador_username" not in session or session["entregador_username"] != username:
        abort(403)

    novo_status = request.form.get('status')
    if novo_status not in ['ativo', 'disponível', 'em rota', 'off-line']:
        return redirect(url_for('entregador.perfil_entregador', username=username, msg="Status inválido"))

    # Busca o entregador
    entregador = entregador_dao.buscar_por_username(username)
    if not entregador:
        abort(404)

    # Atualiza o status
    sucesso = entregador_dao.atualizar_status(entregador['id'], novo_status)

    if sucesso:
        return redirect(url_for('entregador.area_entregador', username=username, msg="Status atualizado com sucesso"))
    else:
        return redirect(url_for('entregador.area_entregador', username=username, msg="Erro ao atualizar status"))
