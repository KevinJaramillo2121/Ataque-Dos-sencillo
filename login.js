// Espera a que todo el contenido del HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {
    
    // Selecciona el formulario y el div para mensajes de error
    const loginForm = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');

    // Escucha el evento 'submit' del formulario
    loginForm.addEventListener('submit', (event) => {
        // Previene que el formulario se envíe de la forma tradicional (recargando la página)
        event.preventDefault();

        // Obtiene los valores de los campos de usuario y contraseña
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Envía los datos al servidor Python usando la API Fetch
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Convierte los datos de JavaScript a un string en formato JSON
            body: JSON.stringify({ username: username, password: password }),
        })
        .then(response => response.text()) // Convierte la respuesta del servidor a texto
        .then(data => {
            if (data === 'success') {
                // Si el servidor responde "success", redirige al panel
                window.location.href = 'panel.html';
            } else {
                // Si no, muestra un mensaje de error
                errorMessageDiv.textContent = 'Usuario o contraseña incorrectos.';
                errorMessageDiv.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessageDiv.textContent = 'Error al conectar con el servidor.';
            errorMessageDiv.style.color = 'red';
        });
    });
});