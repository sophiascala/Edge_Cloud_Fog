import sqlite3

DB_NAME = 'banco_cloud.db'
TEMPO_TESTE = 60
MAQUINAS = 10
TOTAL_LEITURAS_GERADAS = TEMPO_TESTE * MAQUINAS # 600 pacotes trafegados na rede local

def analisar_dados():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT origem, temperatura, tipo_mensagem FROM leituras_consolidadas")
    registros = cursor.fetchall()
    conn.close()
    
    if not registros:
        print("Nenhum dado encontrado no banco. Rode o teste primeiro!")
        return

    total_mensagens_nuvem = len(registros)
    alertas = sum(1 for r in registros if r[2] == 'ALERTA_CRITICO')
    medias = sum(1 for r in registros if r[2] == 'MEDIA_CONSOLIDADA')
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL: INTEGRAÇÃO EDGE-CLOUD (TESTE DE CARGA)")
    print("="*60)
    print(f"⏱️ Tempo de Operação Simulado: {TEMPO_TESTE} Segundos")
    print(f"🏭 Máquinas operando: {MAQUINAS} simultâneas")
    print(f"📡 Dados Brutos Gerados no Chão de Fábrica (Edge): ~{TOTAL_LEITURAS_GERADAS} leituras")
    print("-" * 60)
    print(f"☁️ PAINEL DA NUVEM (CLOUD):")
    print(f"   -> Total de pacotes que chegaram na internet: {total_mensagens_nuvem}")
    print(f"   -> Alertas Críticos (Ação Imediata): {alertas}")
    print(f"   -> Pacotes de Média Consolidada: {medias}")
    print("-" * 60)
    
    # Cálculo de Economia de Banda
    economia = 100 - ((total_mensagens_nuvem / TOTAL_LEITURAS_GERADAS) * 100)
    
    print(f"💰 RESULTADO DO EXPERIMENTO (EFICIÊNCIA DE REDE):")
    print(f"   Sem o Fog, a Nuvem receberia {TOTAL_LEITURAS_GERADAS} pacotes.")
    print(f"   Com o Fog, a Nuvem recebeu apenas {total_mensagens_nuvem} pacotes.")
    print(f"   -> REDUÇÃO DE TRÁFEGO DE BANDA ALCANÇADA: {economia:.1f}%")
    print("="*60 + "\n")

if __name__ == '__main__':
    analisar_dados()