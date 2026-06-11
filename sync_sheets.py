import sqlite3, gspread, time
from oauth2client.service_account import ServiceAccountCredentials

# Configurações do Google
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_JSON = 'credenciais.json' 
PLANILHA_NOME = 'Dados_Fabrica_IoT'

def sincronizar():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_JSON, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(PLANILHA_NOME).sheet1

    while True:
        try:
            conn = sqlite3.connect('banco_cloud.db')
            cursor = conn.cursor()
            cursor.execute("SELECT origem, temperatura, tipo_mensagem, timestamp FROM leituras_consolidadas ORDER BY id DESC LIMIT 50")
            registros = cursor.fetchall()
            conn.close()

            if registros:
                cabecalho = ['Maquina', 'Temperatura', 'Status', 'Timestamp']
                sheet.clear()
                sheet.update('A1', [cabecalho] + [list(r) for r in registros])
                print(f"🔄 Planilha atualizada com os últimos 50 registros.")
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(10) # Atualiza a planilha a cada 10 segundos

if __name__ == '__main__':
    sincronizar()