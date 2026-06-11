import subprocess
import time
import sys

# Lista de scripts que precisam rodar
scripts = [
    "cloud_api.py",
    "fog_node.py",
    "sync_sheets.py",
    "fabrica_edge.py"
]

processos = []

print("🚀 Iniciando ecossistema Edge-Fog-Cloud...")

for script in scripts:
    # Inicia cada script em um processo separado
    p = subprocess.Popen([sys.executable, script])
    processos.append(p)
    print(f"✅ {script} iniciado.")
    time.sleep(2) # Pequena pausa para os servidores subirem em ordem

print("\n🔥 Todos os serviços estão rodando!")
print("Pressione Ctrl+C para encerrar tudo de uma vez.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Encerrando laboratório...")
    for p in processos:
        p.terminate()
    print("Sessão finalizada com sucesso.")