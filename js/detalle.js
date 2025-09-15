import { fetchProducto } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const container = document.getElementById('detalle-container');
  if (!id) {
    container.innerHTML = '<p>ID de producto no especificado.</p>';
    return;
  }
  try {
    const p = await fetchProducto(id);
    container.innerHTML = `
      <h2>${p.nombre}</h2>
      <img src="${p.image_url || 'https://via.placeholder.com/600x400'}" alt="${p.nombre}" />
      <p>${p.description || ''}</p>
      <p><strong>Precio: $${p.precio}</strong></p>
      ${p.video_url ? `<div class="video-embed"><iframe width="560" height="315" src="${p.video_url}" frameborder="0" allowfullscreen></iframe></div>` : ''}
    `;
  } catch (err) {
    container.innerHTML = '<p>Error cargando detalle.</p>';
    console.error(err);
  }
});
