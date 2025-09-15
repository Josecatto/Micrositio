document.addEventListener("DOMContentLoaded", () => {
    // Asumiendo que esta función está en api.js
    const API_URL_BACKEND = "http://127.0.0.1:8000";

    const productosGrid = document.getElementById("productos-grid");

    // Función para obtener y mostrar productos
    async function fetchProductos() {
        try {
            const response = await fetch(`${API_URL_BACKEND}/productos/`);
            if (!response.ok) {
                throw new Error('Error al obtener los productos');
            }
            const productos = await response.json();
            renderProductos(productos);
        } catch (error) {
            console.error("Error:", error);
            productosGrid.innerHTML = "<p>No se pudieron cargar los productos.</p>";
        }
    }

    // Función para renderizar productos
    function renderProductos(productos) {
        productosGrid.innerHTML = ''; // Limpiar la cuadrícula
        if (productos.length === 0) {
            productosGrid.innerHTML = "<p>No hay productos disponibles.</p>";
            return;
        }
        productos.forEach(producto => {
            const productoCard = document.createElement('div');
            productoCard.classList.add('producto-card');
            productoCard.innerHTML = `
                <img src="${producto.image_url}" alt="${producto.nombre}">
                <h3>${producto.nombre}</h3>
                <p>Precio: $${producto.precio}</p>
                <a href="detalle.html?id=${producto.id}">Ver detalles</a>
            `;
            productosGrid.appendChild(productoCard);
        });
    }

    // Llamar a la función al cargar la página
    fetchProductos();
});