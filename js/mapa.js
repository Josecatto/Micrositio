// mapa.js - inicializa Leaflet y muestra un marcador ejemplo
document.addEventListener('DOMContentLoaded', () => {
  const mapDiv = document.getElementById('map');
  if (!mapDiv) return;
  // Crear el mapa centrado en una coordenada de ejemplo
  const script = document.createElement('script');
  script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
  document.body.appendChild(script);
  script.onload = () => {
    const L = window.L;
    const map = L.map('map').setView([4.7109886, -74.072092], 13); // Bogota por defecto
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map);
    L.marker([4.595729060457472, -74.09835428922104]).addTo(map)
      .bindPopup('Resido Aquí').openPopup();
  };
});
