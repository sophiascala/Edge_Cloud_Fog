import time, requests, random, threading
from datetime import datetime

FOG_URL = 'http://127.0.0.1:5000/api/fog'

def maquina(nome):
    while True:
        temp = round(random.uniform(50.0, 110.0), 2)
        try:
            requests.post(FOG_URL, json={"sensor_id": nome, "temperatura": temp, "timestamp": datetime.now().isoformat()})
        except: pass
        time.sleep(random.uniform(0.8, 2.0)) # Cadência realista

if __name__ == '__main__':
    print("🏭 Iniciando 10 Máquinas...")
    for i in range(1, 11):
        threading.Thread(target=maquina, args=(f"Extrusora_{i:02d}",), daemon=True).start()
    while True: time.sleep(1)