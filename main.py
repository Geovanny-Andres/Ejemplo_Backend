# 1) Importación de módulos y funciones necesarios
from functools import lru_cache #Es un decorador que almacena en caché los resultados de una función para que, si se vuelve a llamar con los mismos argumentos, devuelva el resultado almacenado en caché en lugar de volver a calcularlo. 
from typing import Union #Esta es una sugerencia del módulo typing que indica que un valor puede ser uno de varios tipos (por ejemplo, int o None)

from fastapi import FastAPI, Depends #FastAPI: clase principal para crear la app. Depends: sistema de inyección de dependencias (p. ej., entregar la sesión de DB o la config a un endpoint).
from fastapi.responses import PlainTextResponse # PlainTextResponse: construir respuestas de texto plano (útil en handlers de error simples).

# Importa la excepción HTTP de Starlette y la renombra como StarletteHTTPException.
# Esto se usa para registrar un manejador global de errores: @app.exception_handler(StarletteHTTPException)
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware # CORSMiddleware: middleware para habilitar CORS (permitir que el frontend en otro origen/puerto consuma la API).

# routers: comenta la siguiente línea hasta crear la carpeta routers y el archivo todos.py
# routers: comment out next line till create them
from routers import todos

import config # Este es el módulo donde se definen las configuraciones de la aplicación (como las credenciales de la base de datos)

# 2) Creación de la aplicación FastAPI
app = FastAPI() # Esto crea una instancia de una aplicación FastAPI, que manejará las solicitudes HTTP entrantes

# 3) Incluidos los enrutadores (inicialmente comentados)
# router: comment out next line till create it
app.include_router(todos.router) #Incluye un enrutador de un módulo llamado todos.py, que contiene rutas específicas (endpoints) relacionadas con tareas pendientes. Esta línea se comentará hasta que se cree el enrutador.


origins = [
   "http://localhost:3000",
   "http://127.0.0.1:3000",
   "https://modern-todo-frontend-sooty.vercel.app",
]

# 4) Configuración del middleware CORS 
# CORS configuration, needed for frontend development
app.add_middleware( # El middleware es como un intermediario que intercepta y procesa las solicitudes entrantes antes de que lleguen a las rutas de su aplicación.
    CORSMiddleware, # Es un tipo específico de middleware que maneja las reglas CORS (Intercambio de Recursos entre Orígenes) y decide si permitir o bloquear solicitudes provenientes de diferentes dominios
    allow_origins=["*"], # Significa que la API está configurada para aceptar solicitudes de cualquier dominio. Esto es útil durante el desarrollo, cuando el frontend (IU) y el backend (API) podrían ejecutarse en servidores o puertos diferentes
    allow_credentials=True,  # Esto permite que las solicitudes incluyan credenciales como cookies o tokens de autenticación. Es necesario cuando el frontend necesita enviar o recibir datos confidenciales de forma segura
    allow_methods=["*"], # Autoriza todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Autoriza todos los encabezados. Los encabezados suelen contener información importante, como tipos de contenido (JSON, HTML) o tokens de autorización, por lo que permitir todos los encabezados garantiza que no se bloquee nada.
)

# 5) Controlador de excepciones HTTP global 
#Controlador de excepciones global para errores HTTP. Si se produce un error (como un error 404 "No encontrado"), este controlador lo detectará, mostrará el error en la consola y devolverá una respuesta de texto sin formato con los detalles del error.
# global http exception handler, to handle errors
@app.exception_handler(StarletteHTTPException) # Registra un manejador global para errores HTTP (404, 400, etc.)
async def http_exception_handler(request, exc): # request: la petición que falló; exc: la excepción capturada
    print(f"{repr(exc)}") # Logea en consola la excepción completa (útil en desarrollo)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)  # Devuelve una respuesta en texto plano...

#6) Caché de configuración 
#Esta función recupera las configuraciones de la aplicación (del config módulo) y las almacena en caché lru_cachepara evitar cargar repetidamente las configuraciones desde el entorno, lo que mejora el rendimiento.
# to use the settings
@lru_cache()
def get_settings():
    return config.Settings()

# 7) Punto final raíz ("/")
#Esto define el punto final raíz de la API (/). Al acceder a la URL raíz, se imprimirá el nombre de la aplicación desde la configuración y se devolverá "Hola Mundo" como respuesta.
#El settings parámetro se inyecta utilizando el sistema de inyección de dependencia de FastAPI (a través de Depends(get_settings)), lo que permite que la función acceda a la configuración de la aplicación.
@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # print the app_name configuration
    print(settings.app_name)
    return "Hello World"

# 8) Punto final del elemento dinámico ("/items/{item_id}") 
#Esto define un punto final que toma una dinámica item_id en la URL y un parámetro de consulta opcional q.
# Cuando visite /items/123?q=something, devolverá una respuesta JSON con los valores item_idy .q
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}