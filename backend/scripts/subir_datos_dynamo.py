import json
import os
import sys
import time
from decimal import Decimal

# Agregar la carpeta "backend" al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import tabla_juegos

# Ruta al archivo JSON (subimos 2 niveles: scripts/ → backend/ → Amazon-Web-Servicies/)
RUTA_JSON = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "datos",
    "juegos_con_portada.json"
))

print(f"📂 Leyendo JSON desde: {RUTA_JSON}")

# Verificar que el archivo existe
if not os.path.exists(RUTA_JSON):
    print(f"❌ Archivo no encontrado: {RUTA_JSON}")
    print("Verifica que la ruta sea correcta.")
    sys.exit(1)

# Cargar datos del JSON
with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
    juegos = json.load(archivo)

print(f"📊 {len(juegos)} juegos cargados desde JSON")

# Función para convertir floats a Decimal (requerido por DynamoDB)
def convertir_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convertir_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_decimal(i) for i in obj]
    return obj

# Subir a DynamoDB en lotes
print(f"🚀 Subiendo {len(juegos)} juegos a {tabla_juegos.table_name}...")

try:
    LOTE_TAMANO = 20
    total_juegos = len(juegos)
    
    for i in range(0, total_juegos, LOTE_TAMANO):
        lote = juegos[i:i + LOTE_TAMANO]
        
        with tabla_juegos.batch_writer() as batch:
            for juego in lote:
                juego_convertido = convertir_decimal(juego)
                batch.put_item(Item=juego_convertido)
                print(f"  ✅ {juego.get('titulo', 'Sin título')}")
        
        print(f"📦 Lote {i//LOTE_TAMANO + 1}/{(total_juegos + LOTE_TAMANO - 1)//LOTE_TAMANO} completado")
        
        # Esperar 0.5 segundos entre lotes para no saturar la capacidad
        time.sleep(0.5)
    
    print(f"✅ {total_juegos} juegos subidos correctamente a {tabla_juegos.table_name}")

except Exception as e:
    print(f"❌ Error al subir datos: {e}")