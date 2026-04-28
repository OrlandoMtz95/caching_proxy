import sys
from flask import Flask, Response
import requests

app = Flask(__name__)

#ORIGIN = "http://dummyjson.com"

# cache en memoria
cache = {}

origin =""

# Esta linea cpatura cualquier cosa
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # Construir URL destino
    url = f"{origin}/{path}"

    # si ya está en cache
    if url in cache:
        return Response(cache[url], headers={"X-Cache": "HIT"})
    
    # sino está en caché
    # print("CACHE MISS")
    response = requests.get(url)

    # guardar en cache
    cache[url] = response.content

    # Hacer request al servidor real
    #response = requests.get(url)

    # Regresar respuesta al usuario
    return Response(response.content, headers={"X-Cache": "MISS"})

def main():
    global origin
    # limpiar cache
    if "--clear-cache" in sys.argv:
        cache.clear()
        print("Cache limpiada")
        return
    # obtener argumentos
    port = int(sys.argv[sys.argv.index("--port") + 1])
    origin = sys.argv[sys.argv.index("--origin") + 1]

    print(f"Proxy running on port {port} to {origin}")
    app.run(port=port)
    

if __name__ == "__main__":
    main()