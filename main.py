from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
from data.database import database
from data.pelicula_repository import PeliculaRepository
from data.favoritos_repository import FavoritosRepository
from domain.model.Pelicula import Pelicula
from utils.dependencies import require_auth, require_auth_admin
from routers import auth_router, favoritos_router


import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(title="Mi Primera Web FastAPI", description="Ejemplo básico con Jinja2")

# ⭐ IMPORTANTE: Agregar el middleware de sesiones
# Cámbiala clave secreta en producción
app.add_middleware(
    SessionMiddleware,
    secret_key="tu_clave_secreta_muy_segura_cambiala_en_produccion",
    session_cookie="session",
    max_age=3600 * 24 * 7,  # 7 días
    same_site="lax",
    https_only=False  # Cambiar a True en producción con HTTPS
)

# Configurar las plantillas
templates = Jinja2Templates(directory="templatesitos")

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir el router de autenticación
app.include_router(auth_router.router)

# Incluir el router de favoritos
app.include_router(favoritos_router.router)



#RUTA RAIZ
@app.get("/")
async def inicio(request: Request, usuario: dict = Depends(require_auth)):
    """Página de inicio - Requiere autenticación"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuario": usuario
    })

# RUTA INSERTAR PELÍCULA (solo admin)
@app.post("/do_insertar_pelicula")
async def do_insertar_pelicula(
    request: Request,
    titulo: Annotated[str, Form()],
    genero: Annotated[str, Form()],
    año: Annotated[int, Form()],
    director: Annotated[str, Form()],
    imagen: UploadFile = File(None),
    usuario: dict = Depends(require_auth_admin)
):
    """Inserta una película - Solo admin"""
    import os
    import uuid
    
    imagen_path = None
    if imagen and imagen.filename:
        # Generar un nombre único para la imagen
        ext = os.path.splitext(imagen.filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        image_path = os.path.join("static", "images", unique_filename)
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Guardar la imagen
        with open(image_path, "wb") as buffer:
            content = await imagen.read()
            buffer.write(content)
        
        imagen_path = unique_filename
    
    peliculas_repo = PeliculaRepository()
    pelicula = Pelicula(0, titulo, genero, año, director, imagen_path)
    peliculas_repo.insertar_pelicula(database, pelicula)

    return RedirectResponse(url="/", status_code=303)


# FORMULARIO INSERTAR PELÍCULA (solo admin)
@app.get("/insert_pelicula")
async def insert_pelicula(request: Request, usuario: dict = Depends(require_auth_admin)):
    """Formulario para insertar película - Solo admin"""
    return templates.TemplateResponse("insert_pelicula.html", {
        "request": request,
        "usuario": usuario
    })


# RUTA BORRAR PELÍCULA (solo admin)
@app.post("/do_borrar_pelicula")
async def do_borrar_pelicula(
    request: Request,
    id: Annotated[int, Form()],
    usuario: dict = Depends(require_auth_admin)
):
    """Borra una película - Solo admin"""
    peliculas_repo = PeliculaRepository()
    peliculas_repo.borrar_pelicula(database, id)

    return RedirectResponse(url="/", status_code=303)


# RUTA LISTA ACTUALIZAR PELÍCULAS (solo admin)
@app.get("/actualizar_peliculas")
async def lista_actualizar_peliculas(request: Request, usuario: dict = Depends(require_auth_admin)):
    """Lista de películas para actualizar - Solo admin"""
    peliculas_repo = PeliculaRepository()
    peliculas = peliculas_repo.get_all(database)
    
    return templates.TemplateResponse("lista_actualizar_peliculas.html", {
        "request": request,
        "peliculas": peliculas,
        "usuario": usuario
    })


# RUTA FORMULARIO ACTUALIZAR PELÍCULA (solo admin)
@app.get("/actualizar/{id}")
async def actualizar_pelicula(request: Request, id: int, usuario: dict = Depends(require_auth_admin)):
    """Formulario para actualizar película - Solo admin"""
    peliculas_repo = PeliculaRepository()
    pelicula = peliculas_repo.get_by_id(database, id)
    
    return templates.TemplateResponse("actualizar_peliculas.html", {
        "request": request,
        "pelicula": pelicula,
        "usuario": usuario
    })


# RUTA PROCESAR ACTUALIZAR PELÍCULA (solo admin)
@app.post("/do_actualizar_pelicula")
async def do_actualizar_pelicula(
    request: Request,
    id: Annotated[int, Form()],
    titulo: Annotated[str, Form()],
    genero: Annotated[str, Form()],
    año: Annotated[int, Form()],
    director: Annotated[str, Form()],
    usuario: dict = Depends(require_auth_admin)
):
    """Actualiza una película - Solo admin"""
    peliculas_repo = PeliculaRepository()
    pelicula = Pelicula(id, titulo, genero, año, director)
    peliculas_repo.actualizar_pelicula(database, pelicula)

    return RedirectResponse(url="/", status_code=303)


# RUTA FORMULARIO BORRAR PELÍCULAS (solo admin)
@app.get("/borrar")
async def borrar_peliculas(request: Request, usuario: dict = Depends(require_auth_admin)):
    """Formulario para borrar películas - Solo admin"""
    peliculas_repo = PeliculaRepository()
    peliculas = peliculas_repo.get_all(database)

    return templates.TemplateResponse("borrar_peliculas.html", {
        "request": request,
        "peliculas": peliculas,
        "usuario": usuario
    })



# RUTA VER PELÍCULAS (todos los usuarios autenticados)
@app.get("/peliculas", response_class=HTMLResponse)
async def peliculas(request: Request, usuario: dict = Depends(require_auth)):
    """Lista de películas - Todos los usuarios pueden ver"""
    peliculas_repo = PeliculaRepository()
    peliculas = peliculas_repo.get_all(database)

    # Obtener IDs de películas favoritas del usuario
    favoritos_repo = FavoritosRepository()
    favoritos_ids = favoritos_repo.get_favoritos_ids_usuario(database, usuario['user_id'])

    return templates.TemplateResponse("peliculas.html", {
        "request": request,
        "peliculas": peliculas,
        "usuario": usuario,
        "favoritos_ids": favoritos_ids
    })



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
