/**
 * api.js
 * Funciones utilitarias para comunicarse con la API backend.
 * Documentado en español.
 */

const API_BASE = "http://localhost:8000"; // <- Cambiar si tu backend está en otra URL

export async function fetchProductos() {
  const res = await fetch(`${API_BASE}/productos/`);
  if (!res.ok) throw new Error("Error al listar productos");
  return await res.json();
}

export async function fetchProducto(id) {
  const res = await fetch(`${API_BASE}/productos/${id}`);
  if (!res.ok) throw new Error("Producto no encontrado");
  return await res.json();
}

export async function crearProducto(data) {
  const res = await fetch(`${API_BASE}/productos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Error al crear producto: ${txt}`);
  }
  return await res.json();
}

export async function enviarContacto(data) {
  const res = await fetch(`${API_BASE}/contacto/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Error al enviar contacto: ${txt}`);
  }
  return await res.json();
}

export async function significadoNombre(nombre) {
  const form = new FormData();
  form.append("nombre", nombre);
  const res = await fetch(`${API_BASE}/significado-nombre`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Error IA: ${txt}`);
  }
  return await res.json();
}
