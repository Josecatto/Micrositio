// contacto.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contacto-form");
    const resultado = document.getElementById("contacto-resultado");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // 1. Obtener los valores de los campos del formulario
        const nombre = form.querySelector('[name="nombre"]').value;
        const correo = form.querySelector('[name="correo"]').value;
        const mensaje = form.querySelector('[name="mensaje"]').value;

        // 2. Crear un objeto JavaScript con los datos
        const datosContacto = {
            nombre: nombre,
            correo: correo,
            mensaje: mensaje
        };

        try {
            // 3. Enviar los datos como JSON
            const response = await fetch("http://127.0.0.1:8000/contacto/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // ¡Esto es crucial!
                },
                body: JSON.stringify(datosContacto), // Convierte el objeto a una cadena JSON
            });

            if (response.ok) {
                const data = await response.json();
                resultado.innerHTML = `<span style="color: #00ff99;">${data.message}</span>`;
                form.reset();
            } else {
                resultado.innerHTML = `<span style="color: red;">Error al enviar el formulario</span>`;
            }
        } catch (error) {
            resultado.innerHTML = `<span style="color: red;">Error de conexión con el servidor</span>`;
            console.error(error);
        }
    });
});