import os
import json
from typing import List 
from pydantic import BaseModel
from fastapi import FastAPI

#Inicializacion de la aplicacion
app = FastAPI()

#molde de los datos de un juego
class JuegoDTO(BaseModel):
    id: str
    titulo: str
    tipo: str
    modo: str
    plataforma: List[str]
    genero: str
    clasificacion: str
    anio_lanzamiento: int
    calificacion: float
    precio: float

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


#Endpoint[ GET + /]
@app.get("/filtrar")
def filtrar_juegos(
    tipo: Optional[int]= None,
    modo: Optional[str]= None,
    plataforma: Optional[str]= None,
    genero: Optional[str]= None,
    clasificacion: Optional[str]= None,
    anio_lanzamiento: Optional[int]= None,
    calificacion: Optional[float]= None,
    precio: Optional[float]= None):

    #Almacenamos los datos de todos los juegos en un diccionario
    datos_juegos = consultar_juegos()
    
    #Arreglo para almacenar las coincidencias en base a los filtros aplicados
    coincidencias = []

    #Itera sobre cada elemento del datos_juegos(diccionario)
    for diccionario_juego in datos_juegos:
    try:
        #Desempaquetamos el diccionario en un objeto JuegoDTO
        juego = JuegoDTO(**diccionario_juego)
        
        # Proceso de filtrado en base a los datos recibidos en la solicitud GET
        condiciones = [
            not titulo or titulo == juego.titulo,
            not tipo or tipo == juego.tipo,
            not modo or modo == juego.modo,
            not plataforma or plataforma in juego.plataforma,
            not genero or genero == juego.genero,
            not clasificacion or clasificacion == juego.clasificacion,
            not anio_lanzamiento or anio_lanzamiento == juego.anio_lanzamiento,
            not calificacion_min or juego.calificacion >= calificacion_min,
            not precio_max or juego.precio <= precio_max
        ]
    
        # Si todas las condiciones son verdaderas, agregamos el juego a la lista de coincidencias
        if all(condiciones):
            coincidencias.append(juego)
        
    except Exception as e:
        print(f" Error al procesar: {e}")
        
return coincidencias