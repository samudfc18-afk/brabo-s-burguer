from datetime import datetime, time
from zoneinfo import ZoneInfo
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições vindas do Cloudflare Pages

# Fila temporária na memória para armazenar pedidos a serem impressos
pedidos_pendentes = []

def loja_esta_aberta():
    agora_br = datetime.now(ZoneInfo("America/Sao_Paulo"))
    # No Python: 0=Seg, 1=Ter, 2=Qua, 3=Qui, 4=Sex, 5=Sab, 6=Dom
    if agora_br.weekday() == 2:
        return False

    hora_atual = agora_br.time()
    abertura = time(18, 0)
    fechamento = time(23, 30)
    return abertura <= hora_atual <= fechamento

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "aberta": loja_esta_aberta(),
        "mensagem": "API Brabo's Burguer rodando!"
    }), 200

@app.route('/api/pedidos', methods=['POST'])
def receber_pedido():
    if not loja_esta_aberta():
        return jsonify({
            "sucesso": False,
            "erro": "Loja fechada no momento (18h às 23h30, fechado às quartas)."
        }), 403

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    pedidos_pendentes.append(dados)
    print(f"Novo pedido recebido: {dados.get('cliente')}")
    return jsonify({"sucesso": True, "mensagem": "Pedido recebido com sucesso!"}), 201

@app.route('/api/pedidos/pendentes', methods=['GET'])
def listar_pedidos():
    return jsonify(pedidos_pendentes), 200

@app.route('/api/pedidos/limpar', methods=['DELETE'])
def limpar_pedidos():
    pedidos_pendentes.clear()
    return jsonify({"sucesso": True, "mensagem": "Fila limpa"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)