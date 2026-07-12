// script.js
import BASE_URL from './config.js';

document.getElementById('filter-form').addEventListener('submit', function(event) {
    event.preventDefault(); 

    // 1. Capturar los valores del HTML
    const tipo = document.getElementById('tipo').value;
    const modo = document.getElementById('modo').value;
    const plataforma = document.getElementById('plataforma').value;
    const genero = document.getElementById('genero').value;
    const clasificacion = document.getElementById('clasificacion').value;

    const anioRaw = document.getElementById('anio').value;
    const califRaw = document.getElementById('calificacion_min').value;
    const precioRaw = document.getElementById('precio').value;

    // 2. CONSTRUCCIÓN INTELIGENTE DE LA URL (Evita enviar textos vacíos a campos numéricos)
    // Empezamos con los parámetros de texto obligatorios
    let queryParams = `tipo=${tipo}&modo=${modo}&plataforma=${plataforma}&genero=${genero}&clasificacion=${clasificacion}`;

    // Si el usuario escribió un año, lo agregamos con su nombre correcto para tu API
    if (anioRaw !== "") {
        queryParams += `&anio_lanzamiento=${parseInt(anioRaw)}`;
    }

    // Si el usuario escribió calificación, la agregamos como float
    if (califRaw !== "") {
        queryParams += `&calificacion_min=${parseFloat(califRaw)}`;
    }

    // Si el usuario escribió un precio máximo, lo agregamos como float
    if (precioRaw !== "") {
        queryParams += `&precio_max=${parseFloat(precioRaw)}`;
    }

    // Unimos la BASE_URL con la ruta /filtrar y nuestros parámetros limpios
    const url = `${BASE_URL}/filtrar?${queryParams}`;

    console.log("Enviando petición táctica limpia a:", url);

    const container = document.getElementById('juegos-container');
    container.innerHTML = '<p class="placeholder-text"><i class="fa-solid fa-circle-notch fa-spin"></i> Inicializando escáner de base de datos...</p>';

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(juegos => {
            renderizarJuegos(juegos);
        })
        .catch(error => {
            console.error('Error detectado:', error);
            container.innerHTML = '<p class="placeholder-text" style="color: #ef4444; border-color: rgba(239,68,68,0.3);"><i class="fa-solid fa-triangle-exclamation"></i> Error al conectar con el servidor de recomendaciones.</p>';
        });
});

function renderizarJuegos(juegos) {
    const container = document.getElementById('juegos-container');
    container.innerHTML = ''; 

    if (juegos.length === 0) {
        container.innerHTML = '<p class="placeholder-text"><i class="fa-solid fa-radar"></i> No se encontraron juegos que coincidan con esos filtros tácticos.</p>';
        return;
    }

    juegos.forEach(juego => {
        const card = document.createElement('div');
        card.classList.add('juego-card');

        card.innerHTML = `
            <img src="${juego.portada_url || 'https://via.placeholder.com/300x180'}" alt="${juego.titulo}">
            <div class="juego-card-content">
                <h3>${juego.titulo}</h3>
                <div class="tags">
                    <span class="tag"><i class="fa-brands fa-gamepad"></i> ${juego.plataforma.join(', ').toUpperCase()}</span>
                    <span class="tag">${juego.genero.toUpperCase()}</span>
                    <span class="tag">${juego.anio_lanzamiento}</span>
                </div>
                <p>${juego.descripcion || 'Sin análisis operativo disponible para este título.'}</p>
                <div class="juego-footer">
                    <span class="calificacion"><i class="fa-solid fa-star"></i> ${juego.calificacion}</span>
                    <span class="precio">${juego.precio === 0 ? 'GRATIS' : '$' + juego.precio}</span>
                    <a href="${juego.url_juego || '#'}" target="_blank" class="btn-link">ADQUIRIR <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.75rem"></i></a>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}