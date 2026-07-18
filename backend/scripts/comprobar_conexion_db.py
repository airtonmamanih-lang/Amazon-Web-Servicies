import sys
import os

# Agregar la carpeta "backend" al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import tabla_juegos
print("✅ Conectado a DynamoDB")
print(f"📊 Tabla: {tabla_juegos.table_name}")