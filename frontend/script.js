// script.js
import BASE_URL from './config.js';

// ==========================================
// REFERENCIAS DEL FORMULARIO
// ==========================================
const formulario = document.getElementById("filter-form");
const botonBuscar = document.getElementById("btnBuscar");

// Referencia específica al campo de género
const campoGenero = document.getElementById("genero");

// ==========================================
// ACTIVAR / DESACTIVAR BOTÓN (MODIFICADO)
// ==========================================
function actualizarEstadoBoton() {
    // El botón se deshabilita si el valor del género está vacío ("")
    botonBuscar.disabled = (campoGenero.value.trim() === "");
}

// Escuchar cambios únicamente en el campo de género para el estado del botón
campoGenero.addEventListener("input", actualizarEstadoBoton);
campoGenero.addEventListener("change", actualizarEstadoBoton);

// Estado inicial (arrancará bloqueado porque inicia en "")
actualizarEstadoBoton();


// ==========================================
// ENVÍO DEL FORMULARIO
// ==========================================
formulario.addEventListener('submit', function(event) {

    event.preventDefault();

    // Verificación extra por seguridad
    actualizarEstadoBoton();

    if (botonBuscar.disabled) {
        return;
    }

    const filtros = {
        tipo: document.getElementById('tipo').value,
        modo: document.getElementById('modo').value,
        plataforma: document.getElementById('plataforma').value,
        genero: document.getElementById('genero').value,
        clasificacion: document.getElementById('clasificacion').value,
        anio_lanzamiento: document.getElementById('anio').value,
        calificacion_min: document.getElementById('calificacion_min').value,
        precio_max: document.getElementById('precio').value
    };

    const parametrosLimpios = Object.entries(filtros)
        .filter(([_, valor]) => valor !== "")
        .map(([clave, valor]) => `${clave}=${encodeURIComponent(valor)}`)
        .join('&');

    const url = `${BASE_URL}/filtrar?${parametrosLimpios}`;

    console.log("Enviando petición táctica a:", url);

    const container = document.getElementById('juegos-container');

    container.innerHTML =
        '<p class="placeholder-text"><i class="fa-solid fa-circle-notch fa-spin"></i> Inicializando escáner de base de datos...</p>';

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
            container.innerHTML =
                '<p class="placeholder-text" style="color: #ef4444; border-color: rgba(239,68,68,0.3);"><i class="fa-solid fa-triangle-exclamation"></i> Error al conectar con el servidor de recomendaciones.</p>';
        });
});


// ==========================================
// RENDERIZAR JUEGOS
// ==========================================
function renderizarJuegos(juegos) {

    const container = document.getElementById('juegos-container');
    container.innerHTML = '';

    if (juegos.length === 0) {
        container.innerHTML =
            '<p class="placeholder-text"><i class="fa-solid fa-radar"></i> No se encontraron juegos que coincidan con esos filtros tácticos.</p>';
        return;
    }

    juegos.forEach(juego => {
        const card = document.createElement('div');
        card.classList.add('juego-card');

        card.innerHTML = `
            <img src="${juego.portada_url || 'https://dummyimage.com/300x180'}" alt="${juego.titulo}">

            <div class="juego-card-content">

                <h3>${juego.titulo}</h3>

                <div class="tags">
                    <span class="tag">
                        <i class="fa-brands fa-gamepad"></i>
                        ${juego.plataforma.join(', ').toUpperCase()}
                    </span>

                    <span class="tag">
                        ${juego.genero.toUpperCase()}
                    </span>

                    <span class="tag">
                        ${juego.anio_lanzamiento}
                    </span>
                </div>

                <p>
                    ${juego.descripcion || 'Sin análisis operativo disponible para este título.'}
                </p>

                <div class="juego-footer">

                    <span class="calificacion">
                        <i class="fa-solid fa-star"></i>
                        ${juego.calificacion}
                    </span>

                    <span class="precio">
                        ${juego.precio === 0 ? 'GRATIS' : '$' + juego.precio}
                    </span>

                    <a href="${juego.url_juego || '#'}"
                       target="_blank"
                       class="btn-link">
                        ADQUIRIR
                        <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.75rem"></i>
                    </a>

                </div>

            </div>
        `;

        container.appendChild(card);
    });
}