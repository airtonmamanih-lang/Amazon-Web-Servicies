document.getElementById('filter-form').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const tipo = document.getElementById('tipo').value;
    const modo = document.getElementById('modo').value;
    const plataforma = document.getElementById('plataforma').value;
    const genero = document.getElementById('genero').value;
    const clasificacion = document.getElementById('clasificacion').value;
    const anioRango = document.getElementById('anio').value; 
    const calificacionMin = document.getElementById('calificacion_min').value;
    const precio = document.getElementById('precio').value;

    const [anio_inicio, anio_fin] = anioRango.split('-');

    const url = `${BASE_URL}/recomendar?` + 
                `tipo=${tipo}&` +
                `modo=${modo}&` +
                `plataforma=${plataforma}&` +
                `genero=${genero}&` +
                `clasificacion=${clasificacion}&` +
                `anio_inicio=${anio_inicio}&` +
                `anio_fin=${anio_fin}&` +
                `calificacion_min=${calificacionMin}&` +
                `precio=${precio}`;

    console.log("Enviando petición táctica a:", url);

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
                    <span class="tag"><i class="fa-brands fa-gamepad"></i> ${juego.plataforma.toUpperCase()}</span>
                    <span class="tag">${juego.genero.toUpperCase()}</span>
                    <span class="tag">${juego.anio}</span>
                </div>
                <p>${juego.descripcion || 'Sin análisis operativo disponible para este título.'}</p>
                <div class="juego-footer">
                    <span class="calificacion"><i class="fa-solid fa-star"></i> ${juego.calificacion}</span>
                    <span class="precio">${juego.precio.toUpperCase()}</span>
                    <a href="${juego.url_juego}" target="_blank" class="btn-link">ADQUIRIR <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.75rem"></i></a>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}