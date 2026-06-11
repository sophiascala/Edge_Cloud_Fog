from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'banco_cloud.db'

def iniciar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras_consolidadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT, temperatura REAL, tipo_mensagem TEXT, timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/nuvem', methods=['POST'])
def receber_dados_nuvem():
    dados = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO leituras_consolidadas (origem, temperatura, tipo_mensagem, timestamp) VALUES (?, ?, ?, ?)',
                   (dados.get('origem'), dados.get('temperatura'), dados.get('tipo_mensagem'), dados.get('timestamp')))
    conn.commit()
    conn.close()
    print(f"☁️ [CLOUD] {dados.get('tipo_mensagem')} de {dados.get('origem')} armazenado.")
    return jsonify({"status": "ok"}), 201

if __name__ == '__main__':
    iniciar_banco()
    app.run(host='0.0.0.0', port=5001)