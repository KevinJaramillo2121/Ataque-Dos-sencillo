import http.server
import socketserver
import time # Asegúrate de que 'time' esté importado
import os
import json

# --- Configuración del Servidor ---
HOST = "localhost"
PUERTO = 8080

class MiManejador(http.server.SimpleHTTPRequestHandler):
    
    # --- MANEJADOR DE PETICIONES GET (Para servir archivos) ---
    def do_GET(self):
        print(f"¡Petición GET recibida para la ruta: {self.path}!")

        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        if self.path == '/':
            self.path = '/index.html'

        try:
            if os.path.exists(self.path[1:]):
                 super().do_GET()
            else:
                self.send_error(404, "Archivo no encontrado")
        except Exception as e:
            self.send_error(500, f"Error interno del servidor: {e}")

    # --- MANEJADOR DE PETICIONES POST (CON RETARDO PARA DoS) ---
    def do_POST(self):
        print(f"¡Petición POST recibida para la ruta: {self.path}!")

        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            post_data = json.loads(post_data_bytes.decode('utf-8'))
            
            username = post_data.get('username')
            password = post_data.get('password')
            
            print(f"Intento de login con Usuario: {username}, Contraseña: {password}")

            # --- SIMULACIÓN DE CARGA PARA ATAQUE DoS ---
            print("Procesando autenticación (tardará 10 segundos)...")
            time.sleep(5) # AÑADIMOS LA PAUSA DE 10 SEGUNDOS AQUÍ

            # Lógica de autenticación
            authenticated = False
            try:
                with open('usuarios.txt', 'r') as f:
                    for line in f:
                        stored_user, stored_pass = line.strip().split(':')
                        if username == stored_user and password == stored_pass:
                            authenticated = True
                            break
            except FileNotFoundError:
                print("Error: El archivo usuarios.txt no fue encontrado.")

            # Enviar respuesta al cliente (JavaScript)
            if authenticated:
                print("Login EXITOSO.")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'success')
            else:
                print("Login FALLIDO.")
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'failure')
        else:
            self.send_error(404, "Ruta no encontrada para POST")

# --- Iniciamos el servidor ---
with socketserver.TCPServer((HOST, PUERTO), MiManejador) as httpd:
    print(f"Servidor mejorado iniciado en http://{HOST}:{PUERTO}")
    print("Para detener, presiona Ctrl+C")
    httpd.serve_forever()