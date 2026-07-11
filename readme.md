```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FLUJO COMPLETO DEL PROYECTO                     │
│                          (Recomendación de Juegos)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. CLIENTE (Frontend - GitHub Pages)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Usuario selecciona filtros en la interfaz:                                 │
│  ┌──────────────────────────────────────────────────────────────────┐       │ 
│  │  🎮 Recomendación de Juegos                                      │       │
│  │                                                                  │       │
│  │  Tipo:      [Acción ▼]  Modo:      [Multijugador ▼]                      │
│  │  Plataforma:[PC ▼]      Género:    [FPS ▼]                       │       │
│  │  Clasif.:   [M ▼]       Año:       [2020-2024 ▼]                 │       │
│  │  Calif. mín:[4.0 ▼]     Precio:    [Gratis ▼]                    │       │
│  │                                                                  │       │
│  │  [🔍 Buscar Juegos]                                              │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│  JavaScript captura los filtros y construye la URL CON FILTROS:             │
│                                                                             │
│  const url = `https://tu-backend.railway.app/recomendar?` +                 │
│    `tipo=accion&modo=multijugador&plataforma=pc&genero=fps&` +              │
│    `clasificacion=m&anio_inicio=2020&anio_fin=2024&` +                      │
│    `calificacion_min=4&precio=gratis`;                                      │
│                                                                             │
│  fetch(url)  →  Envía petición GET al servidor                              │
│                                                                             │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   │ ① GET /recomendar?tipo=accion&modo=multijugador&...
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. SERVIDOR (Backend - Railway/Render)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Recibe la petición GET y extrae los parámetros:                          │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  tipo           = request.args.get('tipo')           # "accion"  │      │
│  │  modo           = request.args.get('modo')           # "multijugador"│  │
│  │  plataforma     = request.args.get('plataforma')     # "pc"      │      │
│  │  genero         = request.args.get('genero')         # "fps"     │      │
│  │  clasificacion  = request.args.get('clasificacion')  # "m"       │      │
│  │  anio_inicio    = request.args.get('anio_inicio')    # "2020"    │      │
│  │  anio_fin       = request.args.get('anio_fin')       # "2024"    │      │
│  │  calificacion_min= request.args.get('calificacion_min') # "4.0"  │      │
│  │  precio         = request.args.get('precio')         # "gratis"  │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  Construye la consulta a DynamoDB:                                         │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  # Filtros en memoria (ejemplo simplificado)                     │      │
│  │  response = table.scan()                                         │      │
│  │  juegos = response.get('Items', [])                             │      │
│  │                                                                   │      │
│  │  resultados = []                                                 │      │
│  │  for juego in juegos:                                            │      │
│  │      if filtros_coinciden(juego):                                │      │
│  │          resultados.append(juego)                                │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  Responde al cliente con JSON:                                             │
│  return jsonify(resultados)                                               │
│                                                                             │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   │ ② Consulta DynamoDB (scan o query)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. BASE DE DATOS (Amazon DynamoDB)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Tabla: Juegos                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  id       │ titulo              │ tipo   │ modo       │ genero │...   │
│  ├──────────────────────────────────────────────────────────────────┤      │
│  │ juego-001│ Call of Duty        │ accion │ multijugador│ fps   │      │
│  │ juego-002│ Counter-Strike 2    │ accion │ multijugador│ fps   │      │
│  │ juego-003│ FIFA 24             │ deporte│ multijugador│ ...   │      │
│  │ juego-004│ Zelda: Tears        │ aventu │ un jugador  │ ...   │      │
│  │ juego-005│ Fortnite            │ accion │ multijugador│ ...   │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  Devuelve los juegos que coinciden con los filtros:                        │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  Items: [                                                         │      │
│  │    { id: "juego-001", titulo: "Call of Duty", ... },             │      │
│  │    { id: "juego-002", titulo: "Counter-Strike 2", ... },         │      │
│  │    { id: "juego-005", titulo: "Fortnite", ... }                  │      │
│  │  ]                                                               │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   │ ③ Devuelve Items (juegos)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. SERVIDOR → CLIENTE (Respuesta)                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  El servidor formatea la respuesta y la envía al cliente:                 │
│                                                                             │
│  HTTP/1.1 200 OK                                                           │
│  Content-Type: application/json                                            │
│                                                                             │
│  [                                                                         │
│    {                                                                       │
│      "id": "juego-001",                                                    │
│      "titulo": "Call of Duty: Warzone",                                    │
│      "tipo": "accion",                                                     │
│      "modo": "multijugador",                                               │
│      "plataforma": "pc",                                                   │
│      "genero": "fps",                                                      │
│      "clasificacion": "m",                                                 │
│      "anio": 2022,                                                         │
│      "calificacion": 4.5,                                                  │
│      "precio": "gratis",                                                   │
│      "descripcion": "Battle royale intenso con hasta 150 jugadores...",   │
│      "portada_url": "https://imagenes.com/call-of-duty.jpg",               │
│      "url_juego": "https://play.callofduty.com"                           │
│    },                                                                      │
│    {                                                                       │
│      "id": "juego-002",                                                    │
│      "titulo": "Counter-Strike 2",                                         │
│      "tipo": "accion",                                                     │
│      "modo": "multijugador",                                               │
│      "plataforma": "pc",                                                   │
│      "genero": "fps",                                                      │
│      "clasificacion": "m",                                                 │
│      "anio": 2023,                                                         │
│      "calificacion": 4.8,                                                  │
│      "precio": "gratis",                                                   │
│      "descripcion": "El clásico FPS competitivo renovado...",             │
│      "portada_url": "https://imagenes.com/cs2.jpg",                        │
│      "url_juego": "https://counter-strike.net"                            │
│    }                                                                       │
│  ]                                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

diseno visual sugerido
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🎮 Recomendación de Juegos                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Tipo:     [Acción ▼]   Modo:     [Multijugador ▼]                       │
│  Plataforma: [PC ▼]     Género:   [FPS ▼]                                │
│  Clasificación: [M ▼]   Año:      [2020 ▼] - [2024 ▼]                   │
│  Calif. mín: [4.0 ▼]    Precio:   [Gratis ▼]                             │
│                                                                             │
│  [ 🔍 Buscar Juegos ]                                                      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Resultados (3 juegos encontrados)                                        │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  📸                                                               │    │
│  │  [Portada]    Call of Duty: Warzone                               │    │
│  │               ⭐ 4.5/5  •  Acción  •  Multijugador  •  PC        │    │
│  │               FPS  •  M (17+)  •  2022  •  Gratis                │    │
│  │               "Battle royale intenso con hasta 150 jugadores..."  │    │
│  │               [🔗 Jugar ahora]                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  📸                                                               │    │
│  │  [Portada]    Counter-Strike 2                                    │    │
│  │               ⭐ 4.8/5  •  Acción  •  Multijugador  •  PC        │    │
│  │               FPS  •  M (17+)  •  2023  •  Gratis                │    │
│  │               "El clásico FPS competitivo renovado..."            │    │
│  │               [🔗 Jugar ahora]                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  📸                                                               │    │
│  │  [Portada]    Fortnite                                             │    │
│  │               ⭐ 4.2/5  •  Acción  •  Multijugador  •  PC        │    │
│  │               Battle Royale  •  T (13+)  •  2017  •  Gratis      │    │
│  │               "Construye, lucha y sobrevive en un mundo..."       │    │
│  │               [🔗 Jugar ahora]                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Para cada juego, mostrar:

|Elemento|De dónde sale|Ejemplo|
|---|---|---|
|**Portada**|`portada_url`|`<img src="https://...">`|
|**Título**|`titulo`|"Call of Duty: Warzone"|
|**Tipo**|`tipo`|"Acción"|
|**Modo**|`modo`|"Multijugador"|
|**Plataforma**|`plataforma`|"PC"|
|**Género**|`genero`|"FPS"|
|**Clasificación**|`clasificacion`|"M (17+)"|
|**Año**|`anio`|2022|
|**Calificación**|`calificacion`|⭐ 4.5/5|
|**Precio**|`precio`|"Gratis"|
|**Descripción**|`descripcion`|"Battle royale intenso..."|
|**Enlace**|`url_juego`|`<a href="...">Jugar ahora</a>`|

### 📋 Resumen

|Aspecto|Detalle|
|---|---|
|**Método**|`GET`|
|**Endpoint**|`https://tu-backend.railway.app/recomendar`|
|**Parámetros**|8 filtros (ver tabla arriba)|
|**Respuesta**|Array JSON con objetos de juegos|
|**Campos de respuesta**|`id`, `titulo`, `tipo`, `modo`, `plataforma`, `genero`, `clasificacion`, `anio`, `calificacion`, `precio`, `descripcion`, `portada_url`, `url_juego`|
