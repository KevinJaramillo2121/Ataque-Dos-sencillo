import http.server
import socketserver
import time
import os

# --- Configuración del Servidor ---
HOST = "localhost"
PUERTO = 8080

class MiManejador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"¡Petición recibida para la ruta: {self.path}!")

        # --- NUEVA SECCIÓN ---
        # Si el navegador pide el favicon, le decimos que no hay contenido y terminamos.
        # Esto evita el error 404 y el retardo de 10 segundos para esta petición.
        if self.path == '/favicon.ico':
            self.send_response(204)  # 204 significa "No Content" (Sin Contenido)
            self.end_headers()
            return  # Detiene la ejecución aquí mismo para no continuar

        # --- El código anterior continúa aquí ---
        # Esta parte solo se ejecutará para peticiones que NO sean para el favicon.
        print("El servidor está procesando una tarea pesada...")
        time.sleep(3)

        if self.path == '/':
            self.path = '/index.html'

        try:
            # Comprueba si el archivo existe y lo envía
            if os.path.exists(self.path[1:]):
                 super().do_GET()
                 print("Página y recursos enviados correctamente.")
            else:
                self.send_error(404, "Archivo no encontrado")
                print(f"Error: Archivo no encontrado en la ruta '{self.path}'.")

        except Exception as e:
            self.send_error(500, f"Error interno del servidor: {e}")
            print(f"Error al servir la petición: {e}")


# --- Iniciamos el servidor ---
with socketserver.TCPServer((HOST, PUERTO), MiManejador) as httpd:
    print(f"Servidor mejorado iniciado en http://{HOST}:{PUERTO}")
    print("Para detener, presiona Ctrl+C")
    httpd.serve_forever()