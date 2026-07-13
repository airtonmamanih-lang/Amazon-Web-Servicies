import os
import json
import time
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# Rutas de archivos
RUTA_ORIGINAL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datos", "juegos.json"))
RUTA_DESTINO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datos", "juegos_hidratados.json"))

def hidratar_base_datos():
    # 1. Leer los juegos que no tienen portada
    try:
        with open(RUTA_ORIGINAL, "r", encoding="utf-8") as archivo:
            juegos = json.load(archivo)
    except FileNotFoundError:
        print("No se encontró el archivo original.")
        return

    API_KEY_RAWG = os.getenv("API_KEY_RAWG")
    juegos_procesados = []
    
    print(f"Iniciando hidratación de {len(juegos)} juegos...")

    # 2. Bucle controlado (Corre una sola vez para toda tu base de datos)
    for juego in juegos:
        # Si ya tiene una portada válida, no le pegamos a la API de nuevo
        if juego.get("portada_url"):
            juegos_procesados.append(juego)
            continue
            
        titulo = juego.get("titulo")
        print(f"Buscando portada para: {titulo}...")
        
        try:
            titulo_codificado = urllib.parse.quote(titulo)
            url_rawg = f"https://api.rawg.io/api/games?key={API_KEY_RAWG}&search={titulo_codificado}"
            
            with urllib.request.urlopen(url_rawg, timeout=5) as response:
                res_data = json.loads(response.read().decode())
                
                if res_data.get("results") and len(res_data["results"]) > 0:
                    # Extraemos la imagen y la inyectamos permanentemente en el diccionario
                    juego["portada_url"] = res_data["results"][0].get("background_image")
                    print(f" -> ¡Portada encontrada!")
                else:
                    juego["portada_url"] = None
                    print(f" -> No se encontraron resultados en RAWG.")
                    
        except Exception as err:
            print(f" -> Error al consultar RAWG para {titulo}: {err}")
            juego["portada_url"] = None

        juegos_procesados.append(juego)
        
        # TRUCO DE INGENIERÍA: Rate Limiting
        # Dejar descansar la API 0.5 segundos entre juegos para evitar bloqueos por IP (HTTP 429 Too Many Requests)
        time.sleep(0.5)

    # 3. Guardar el nuevo JSON con los datos listos de forma permanente
    with open(RUTA_DESTINO, "w", encoding="utf-8") as archivo:
        json.dump(juegos_procesados, archivo, indent=4, ensure_ascii=False)
        
    print(f"¡Proceso terminado! Archivo guardado en: {RUTA_DESTINO}")

if __name__ == "__main__":
    hidratar_base_datos()