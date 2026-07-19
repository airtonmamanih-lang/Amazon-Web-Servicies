# verificar_tabla.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.database import tabla_juegos

print(f"📊 Nombre de la tabla en tu código: {tabla_juegos.table_name}")

# Intentar leer un juego
response = tabla_juegos.scan(Limit=1)
items = response.get('Items', [])
print(f"📚 Juegos encontrados: {len(items)}")
if items:
    print(f"  Primer juego: {items[0].get('titulo', 'Sin título')}")