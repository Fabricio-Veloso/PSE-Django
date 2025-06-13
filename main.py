# main.py

import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

# Configuração de log persistente
logging.basicConfig(
    filename='/app/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_data():
    try:
        conn = psycopg2.connect(
            dbname="teste_db",
            user="teste_user",
            password="senha123",
            host="host.docker.internal",  # ou IP da máquina
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes;")
        rows = cur.fetchall()
        logging.info("Consulta realizada com sucesso.")
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Erro ao acessar o banco: {e}")
        return []

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/dados':
            data = get_data()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    logging.info("Servidor iniciado na porta 8000.")
    server = HTTPServer(('', 8000), SimpleHandler)
    server.serve_forever()

