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
    tipo: Optional[str]= None,
    modo: Optional[str]= None,
    plataforma: Optional[str]= None,
    genero: Optional[str]= None,
    clasificacion: Optional[str]= None,
    anio_lanzamiento: Optional[int]= None,
    calificacion: Optional[float]= None,
    precio: Optional[float]= None):

    #Almacenamos los datos de todos los juegos en una variable
    datos_juegos = consultar_juegos()
    
    #Variable para almacenar las coincidencias en base a los filtros aplicados
    coincidencias = []

    if all(coincidencias):
        coincidencias.append(juego)