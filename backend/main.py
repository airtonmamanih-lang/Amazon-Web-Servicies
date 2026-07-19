import os
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config.database import tabla_juegos

# Inicializacion de la aplicacion
app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Consulta a DynamoDB por género
def consultar_juegos_por_genero(genero: str):
    try:
        response = tabla_juegos.query(
            IndexName='genero_index',
            KeyConditionExpression='genero = :genero',
            ExpressionAttributeValues={':genero': genero}
        )
        return response.get('Items', [])
    except Exception as e:
        print(f"Error al consultar DynamoDB: {e}")
        return []

# Endpoint [GET /filtrar]
@app.get("/filtrar")
def filtrar_juegos(
    genero: str,    
    tipo: Optional[str] = None,
    modo: Optional[str] = None,
    plataforma: Optional[str] = None,
    clasificacion: Optional[str] = None,
    anio_lanzamiento: Optional[int] = None,
    calificacion_min: Optional[float] = None,
    precio_max: Optional[float] = None
):
    # Obtener juegos de DynamoDB SOLO por género
    datos_juegos = consultar_juegos_por_genero(genero)
    
    if not datos_juegos:
        return []
    
    coincidencias = []
    for diccionario_juego in datos_juegos:
        try:
            juego = JuegoDTO(**diccionario_juego)
            
            condiciones = [
                not tipo or tipo == juego.tipo,
                not modo or modo == juego.modo,
                not plataforma or plataforma in juego.plataforma,
                not clasificacion or clasificacion == juego.clasificacion,
                not anio_lanzamiento or anio_lanzamiento == juego.anio_lanzamiento,
                not calificacion_min or juego.calificacion >= calificacion_min,
                not precio_max or juego.precio <= precio_max
            ]
            
            if all(condiciones):
                coincidencias.append(juego)
        except Exception as e:
            print(f"Error al procesar un registro: {e}")    
            
    return coincidencias