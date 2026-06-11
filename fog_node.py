from flask import Flask, request, jsonify
import requests, time
from datetime import datetime

app = Flask(__name__)
CLOUD_URL = 'http://127.0.0.1:5001/api/nuvem'
leituras_temporarias = {}

@app.route('/api/fog', methods=['POST'])
def receber_dados_edge():
    global leituras_temporarias
    dado_bruto = request.json
    
    sid = dado_bruto['sensor_id']
    temp = dado_bruto['temperatura']
    
    if sid not in leituras_temporarias: 
        leituras_temporarias[sid] = []

    if temp > 85.0:
        # ALERTA CRÍTICO
        print(f"\033[91m🚨 [CRÍTICO] {sid}: {temp}°C! Enviando à Cloud...\033[0m")
        
        payload = {
            "origem": sid, 
            "temperatura": temp, 
            "tipo_mensagem": "ALERTA_CRITICO", 
            "timestamp": datetime.now().isoformat()
        }
        requests.post(CLOUD_URL, json=payload)
        
    else:
        # LEITURA NORMAL
        leituras_temporarias[sid].append(temp)
        print(f"\033[92m✅ [NORMAL] {sid}: {temp}°C registrado no Fog.\033[0m")
        
        if len(leituras_temporarias[sid]) >= 5:
            media = round(sum(leituras_temporarias[sid])/5, 2)
            
            payload = {
                "origem": sid, 
                "temperatura": media, 
                "tipo_mensagem": "MEDIA_CONSOLIDADA", 
                "timestamp": datetime.now().isoformat()
            }
            requests.post(CLOUD_URL, json=payload)
            
            print(f"\033[94m☁️ [FOG] Média {sid} ({media}°C) enviada à Cloud.\033[0m")
            leituras_temporarias[sid] = []
            
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    print("\033[93m🌫️ Servidor FOG (Névoa) INICIADO (Modo Silencioso). Monitorando fábrica...\033[0m")
    app.run(host='0.0.0.0', port=5000)