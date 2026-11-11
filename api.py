from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições vindas do Cloudflare Pages

# Fila temporária na memória para armazenar pedidos a serem impressos
pedidos_pendentes = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "mensagem": "API Brabo's Burguer rodando!"}), 200

@app.route('/api/pedidos', methods=['POST'])
def receber_pedido():
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