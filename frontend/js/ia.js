import { significadoNombre } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('ia-form');
  const out = document.getElementById('ia-output');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nombre = form.nombre.value;
    try {
      const res = await significadoNombre(nombre);
      out.textContent = `Significado de ${res.nombre}: ${res.significado}`;
    } catch (err) {
      out.textContent = 'Error al obtener significado.';
      console.error(err);
    }
  });
});
