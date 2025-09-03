# 🐌 SlowLogin DoS - Laboratorio Educativo 🐌

![Banner del Proyecto](https_URL_DE_TU_BANNER_AQUI)

**Bienvenido a SlowLogin DoS, un laboratorio práctico diseñado para demostrar un ataque de Denegación de Servicio (DoS) a nivel de aplicación (Capa 7) explotando un proceso de autenticación lento.**

Este proyecto contiene todos los componentes necesarios para simular un escenario realista en un entorno local y seguro:
* Un **servidor web vulnerable** en Python.
* Una **interfaz de login** funcional (HTML/CSS/JS).
* Un **script de ataque** simple para agotar los recursos del servidor.

---

## ⚠️ ¡Advertencia y Uso Ético! ⚠️

Este software ha sido creado **única y exclusivamente con fines educativos**. El objetivo es entender una vulnerabilidad común para aprender a defenderse de ella.

**NO UTILICES** estas herramientas contra ningún sistema que no sea de tu propiedad o para el cual no tengas permiso explícito. El uso no autorizado es **ilegal**. Eres el único responsable de tus acciones.

---

## 🔬 Concepto del Laboratorio

A diferencia de los ataques DoS que buscan saturar el ancho de banda de una red, este laboratorio se centra en un ataque a la **capa de aplicación**. El objetivo es agotar los recursos del servidor (como la memoria o los hilos de procesamiento) con solicitudes que parecen legítimas pero que son computacionalmente costosas para el servidor.

### La Vulnerabilidad: El Login Lento

El corazón de este laboratorio es el archivo `servidor.py`. Este servidor tiene una ruta de login (`/login`) que, de forma intencionada, simula un proceso de autenticación muy lento (por ejemplo, una consulta a una base de datos compleja o un cálculo criptográfico pesado).

```python
# Dentro de servidor.py
def do_POST(self):
    if self.path == '/login':
        # ... lógica de autenticación ...

        # --- SIMULACIÓN DE CARGA PARA ATAQUE DoS ---
        print("Procesando autenticación (tardará 5 segundos)...")
        time.sleep(5) # ¡AQUÍ ESTÁ LA VULNERABILIDAD!
Cada vez que un usuario intenta iniciar sesión, el servidor se queda "ocupado" durante 5 segundos. Un usuario normal no lo notaría demasiado, pero ¿qué pasa si muchos "usuarios" intentan iniciar sesión al mismo tiempo?

El Ataque: Agotamiento de Recursos
El script ataque.py es nuestra herramienta para explotar esta vulnerabilidad. Crea cientos o miles de hilos, y cada uno intenta establecer una conexión con el servidor. Al mantener estas conexiones abiertas y forzar al servidor a procesar múltiples logins "lentos" de forma simultánea, agotamos su capacidad para atender a usuarios legítimos.

El resultado: el servidor deja de responder.

Diagrama del Escenario
      +----------------+
      |                |
      |   ATACANTE     |
      |  (ataque.py)   |
      |                |
      +-------+--------+
              |
              | Múltiples conexiones simultáneas
              | (GET /)
              v
      +-------+--------+
      |                |
      | SERVIDOR VÍCTIMA|  <-- Cada conexión consume un hilo
      |  (servidor.py) |      y espera 5s en el login,
      |                |      agotando los recursos.
      +----------------+
🚀 Puesta en Marcha
Sigue estos pasos para montar el laboratorio en tu máquina.

✅ Prerrequisitos
Python 3.x.

⚙️ Configuración
Clona el repositorio:

Bash

git clone [https://github.com/](https://github.com/)[TU_USUARIO]/[NOMBRE_DEL_REPOSITORIO].git
cd [NOMBRE_DEL_REPOSITORIO]
Crea el archivo de usuarios:
El servidor necesita un archivo usuarios.txt para verificar las credenciales. Crea este archivo en la misma carpeta con el siguiente formato:

usuario:contraseña
Por ejemplo:

admin:1234
user:password
📂 Estructura de Archivos
Asegúrate de que tu directorio tenga esta estructura:

.
├── ataque.py         # El script atacante
├── servidor.py       # El servidor web vulnerable
├── index.html        # La página de login
├── panel.html        # La página de bienvenida tras el login
├── login.js          # Lógica del formulario de login
├── estilos.css       # Estilos visuales
└── usuarios.txt      # Archivo de credenciales
🎮 Ejecutando la Simulación (Paso a Paso)
Para observar el ataque, necesitarás tener dos terminales o consolas abiertas.

Paso 1: Iniciar el Servidor Vulnerable
En tu primera terminal, ejecuta el servidor:

Bash

python servidor.py
Deberías ver un mensaje como este, indicando que el servidor está listo:

Servidor mejorado iniciado en http://localhost:8080
Para detener, presiona Ctrl+C
Paso 2: Verificar el Funcionamiento Normal
Abre tu navegador web y ve a http://localhost:8080.
Verás el formulario de login. Intenta iniciar sesión con un usuario y contraseña válidos (los que pusiste en usuarios.txt). Deberías ser redirigido al panel.html después de una pequeña espera. ¡El servidor funciona!

Paso 3: Lanzar el Ataque
Ahora, en tu segunda terminal, ejecuta el script de ataque:

Bash

python ataque.py
Verás cómo la terminal empieza a llenarse de mensajes de "Conexión establecida" o errores si el servidor ya está saturado.

Paso 4: Observar los Efectos del DoS
Vuelve a tu navegador e intenta hacer una de estas acciones:

Recargar la página http://localhost:8080.

Abrir una nueva pestaña e intentar acceder.

notarás que la página carga indefinidamente o muestra un error de "tiempo de espera agotado". En la terminal del servidor, verás el flujo constante de peticiones.

¡Has logrado una Denegación de Servicio! El servidor está tan ocupado con las peticiones del atacante que no puede atender a tu solicitud legítima desde el navegador.

Para detener todo, presiona Ctrl+C en ambas terminales.

🛡️ ¿Cómo nos Defendemos? (Mitigación)
Entender el ataque es solo la mitad del camino. ¿Cómo podría "SecureCorp" proteger su servidor?

Rate Limiting (Limitación de Tasa): Es la defensa más efectiva para este escenario. Consiste en limitar el número de intentos de login desde una misma dirección IP en un período de tiempo. Por ejemplo: "Máximo 5 intentos de login por minuto desde esta IP".

Workers Asíncronos: Utilizar un servidor web moderno (como Gunicorn con workers de tipo gevent o uvicorn) que no se bloquee con operaciones lentas. Una solicitud lenta no impediría que otras más rápidas se procesen.

Optimización del Proceso Lento: La solución de raíz es mejorar el rendimiento del proceso de autenticación para que no tarde 5 segundos.

CAPTCHA: Implementar un CAPTCHA después de varios intentos fallidos para asegurarse de que la solicitud proviene de un humano y no de un bot.

🤝 Contribuciones
Si tienes ideas para mejorar este laboratorio, ¡toda contribución es bienvenida! Simplemente haz un fork y envía un Pull Request.

<p align="center">
Hecho con 🐍 y con fines educativos por [Kevin Villada Jaramillo - KevinJaramillo2121]
</p>
