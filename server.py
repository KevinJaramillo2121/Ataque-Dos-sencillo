import http.server
import socketserver
import time

# --- Configuración del Servidor ---
HOST = "localhost"  # Escuchará solo en tu máquina local
PUERTO = 8080

# Esta clase maneja las peticiones que llegan al servidor
class MiManejador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"¡Petición recibida de {self.client_address[0]}!")
        
        # Simulamos que la página tarda en cargar para hacer el efecto más visible
        time.sleep(5) 
        
        # Respuesta que se envía al navegador
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hola, esta es la pagina.</h1></body></html>")
        print("Respuesta enviada.")

# --- Iniciamos el servidor ---
with socketserver.TCPServer((HOST, PUERTO), MiManejador) as httpd:
    print(f"Servidor iniciado en http://{HOST}:{PUERTO}")
    print("Esperando conexiones... (Para detener, presiona Ctrl+C)")
    
    # El servidor se queda escuchando para siempre
    httpd.serve_forever()