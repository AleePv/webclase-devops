from typing import Annotated
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.favoritos_repository import FavoritosRepository
from data.pelicula_repository import PeliculaRepository
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/favoritos", tags=["favoritos"])

templates = Jinja2Templates(directory="templatesitos")


@router.get("/mis-favoritos", response_class=HTMLResponse)
async def mis_favoritos(request: Request, usuario: dict = Depends(require_auth)):
    favoritos_repo = FavoritosRepository()
    favoritos = favoritos_repo.get_favoritos_usuario(database, usuario['user_id'])
    
    return templates.TemplateResponse("mis_favoritos.html", {
        "request": request,
        "usuario": usuario,
        "favoritos": favoritos
    })


@router.post("/agregar/{pelicula_id}")
async def agregar_favorito(
    request: Request,
    pelicula_id: int,
    usuario: dict = Depends(require_auth)
):
    form = await request.form()
    comentario = form.get('comentario', '')
    stars = int(form.get('stars', 0))
    
    try:
        favoritos_repo = FavoritosRepository()
        pelicula_repo = PeliculaRepository()
        
        pelicula = pelicula_repo.get_by_id(database, pelicula_id)
        if not pelicula:
            return RedirectResponse(url="/peliculas", status_code=303)
        
        favoritos_repo.agregar_favorito(database, usuario['user_id'], pelicula_id, comentario, stars)
        
        return RedirectResponse(url="/peliculas", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/peliculas", status_code=303)


@router.post("/quitar/{pelicula_id}")
async def quitar_favorito(
    request: Request,
    pelicula_id: int,
    usuario: dict = Depends(require_auth)
):
    favoritos_repo = FavoritosRepository()
    favoritos_repo.quitar_favorito(database, usuario['user_id'], pelicula_id)
    
    referer = request.headers.get("referer", "/peliculas")
    if "mis-favoritos" in referer:
        return RedirectResponse(url="/favoritos/mis-favoritos", status_code=303)
    else:
        return RedirectResponse(url="/peliculas", status_code=303)


@router.post("/editar/{pelicula_id}")
async def editar_favorito(
    request: Request,
    pelicula_id: int,
    usuario: dict = Depends(require_auth)
):
    form = await request.form()
    comentario = form.get('comentario', '')
    stars = int(form.get('stars', 0))
    
    try:
        favoritos_repo = FavoritosRepository()
        favoritos_repo.actualizar_favorito(database, usuario['user_id'], pelicula_id, comentario, stars)
        
        return RedirectResponse(url="/favoritos/mis-favoritos", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/favoritos/mis-favoritos", status_code=303)


@router.get("/admin/todos-favoritos", response_class=HTMLResponse)
async def admin_todos_favoritos(request: Request, usuario: dict = Depends(require_auth_admin)):
    favoritos_repo = FavoritosRepository()
    todos_favoritos = favoritos_repo.get_todos_favoritos(database)
    
    return templates.TemplateResponse("admin_favoritos.html", {
        "request": request,
        "usuario": usuario,
        "favoritos": todos_favoritos
    })
