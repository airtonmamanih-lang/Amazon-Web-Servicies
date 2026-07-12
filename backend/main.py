import os
import json
import urllib.request
import urllib.parse
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializacion de la aplicacion
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Abre la frontera para que tu Front local pueda consultar
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Molde de los datos de un juego
class JuegoDTO(BaseModel):
    id: int
    titulo: str
    tipo: str
    modo: str
    plataforma: List[str]
    genero: str
    clasificacion: str
    anio_lanzamiento: int
    calificacion: float
    precio: float
    portada_url: Optional[str] = None
    descripcion: str
    url_juego: str

# Calculamos la ruta subiendo un nivel y entrando a la carpeta 'datos'
RUTA_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "datos", "juegos.json"))

# Consulta de todos los juegos a juegos.json
def consultar_juegos():
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        return {"error": "Archivo no encontrado"}
    except json.JSONDecodeError:
        return {"error": "Error al decodificar el archivo JSON"}


# Endpoint [GET /filtrar]
@app.get("/filtrar")
def filtrar_juegos(
    tipo: Optional[str] = None,
    modo: Optional[str] = None,
    plataforma: Optional[str] = None,
    genero: Optional[str] = None,
    clasificacion: Optional[str] = None,
    anio_lanzamiento: Optional[int] = None,
    calificacion_min: Optional[float] = None,
    precio_max: Optional[float] = None
):
    
    # Almacenamos los datos de todos los juegos
    datos_juegos = consultar_juegos()
    
    # Si hay error al cargar el JSON, retornamos el error
    if isinstance(datos_juegos, dict) and "error" in datos_juegos:
        return datos_juegos
    
    # Arreglo para almacenar las coincidencias en base a los filtros aplicados
    coincidencias = []

    API_KEY_RAWG = "daa2bf37ba9b4ce89dc30fa246f4fb0f"

    # Itera sobre cada elemento del datos_juegos
    for diccionario_juego in datos_juegos:
        try:
            # Desempaquetamos el diccionario en un objeto JuegoDTO
            juego = JuegoDTO(**diccionario_juego)

            condiciones = [
                not tipo or tipo == juego.tipo,
                not modo or modo == juego.modo,
                not plataforma or plataforma in juego.plataforma,
                not genero or genero == juego.genero,
                not clasificacion or clasificacion == juego.clasificacion,
                not anio_lanzamiento or anio_lanzamiento == juego.anio_lanzamiento,
                not calificacion_min or juego.calificacion >= calificacion_min,
                not precio_max or juego.precio <= precio_max
            ]


            # Si todas las condiciones son verdaderas
            if all(condiciones):
                try:
                    # Codificamos el título para la URL externa
                    titulo_codificado = urllib.parse.quote(juego.titulo)
                    url_rawg = f"https://api.rawg.io/api/games?key={API_KEY_RAWG}&search={titulo_codificado}"
                    
                    # Llamada a la API externa de RAWG
                    with urllib.request.urlopen(url_rawg, timeout=5) as response:
                        res_data = json.loads(response.read().decode())
                        
                        if res_data.get("results") and len(res_data["results"]) > 0:
                            juego.portada_url = res_data["results"][0].get("background_image")
                            
                except Exception as api_err:
                    print(f"No se pudo obtener portada para {juego.titulo}: {api_err}")
                    juego.portada_url = None 

                #  Mete el juego ya procesado con su imagen inyectada
                coincidencias.append(juego)
                
        except Exception as e:
            print(f"Error al procesar un registro: {e}")    
            
    return coincidencias