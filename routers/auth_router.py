from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.usuario_repository import UsuarioRepository
from utils.session import crear_sesion, destruir_sesion, obtener_usuario_actual

# Crear el router
router = APIRouter(prefix="/auth", tags=["autenticacion"])

# Configurar las plantillas
templates = Jinja2Templates(directory="templatesitos")


@router.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    """Muestra el formulario de login"""
    # Si ya está autenticado, redirigir al inicio
    usuario = obtener_usuario_actual(request)
    if usuario:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None
    })

@router.get("/prohibido", response_class=HTMLResponse)
async def mostrar_403(request: Request):
    """Muestra el formulario de login"""
    
    return templates.TemplateResponse("403.html", {
        "request": request,
        "error": None
    })


@router.post("/login")
async def do_login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """Procesa el login"""
    usuario_repo = UsuarioRepository()
    
    # Buscar el usuario
    usuario = usuario_repo.get_by_username(database, username)
    
    if not usuario:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Usuario o contraseña incorrectos",
            "username": username
        })
    
    # Verificar la contraseña
    if not usuario_repo.verificar_password(password, usuario.password_hash):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Usuario o contraseña incorrectos",
            "username": username
        })
    
    # Crear sesión con is_admin
    crear_sesion(request, usuario.id, usuario.username, usuario.is_admin)
    
    # Redirigir al inicio
    return RedirectResponse(url="/", status_code=303)


@router.get("/registro", response_class=HTMLResponse)
async def mostrar_registro(request: Request):
    """Muestra el formulario de registro"""
    # Si ya está autenticado, redirigir al inicio
    usuario = obtener_usuario_actual(request)
    if usuario:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("registro.html", {
        "request": request,
        "error": None
    })


@router.post("/registro")
async def do_registro(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirm: Annotated[str, Form()],
    email: Annotated[str, Form()] = None
):
    """Procesa el registro de usuario"""
    usuario_repo = UsuarioRepository()
    
    # Validaciones
    if not username or len(username) < 3:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "El nombre de usuario debe tener al menos 3 caracteres",
            "username": username,
            "email": email
        })
    
    if not password or len(password) < 6:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "La contraseña debe tener al menos 6 caracteres",
            "username": username,
            "email": email
        })
    
    if password != password_confirm:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "Las contraseñas no coinciden",
            "username": username,
            "email": email
        })
    
    # Verificar que el usuario no exista
    usuario_existente = usuario_repo.get_by_username(database, username)
    if usuario_existente:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": "El nombre de usuario ya existe",
            "username": username,
            "email": email
        })
    
    # Insertar el usuario (por defecto is_admin=False)
    try:
        usuario_repo.insertar_usuario(database, username, password, email, is_admin=False)
        
        # Obtener el usuario recién creado para crear la sesión
        usuario = usuario_repo.get_by_username(database, username)
        
        # Crear sesión con el campo is_admin del usuario
        crear_sesion(request, usuario.id, usuario.username, usuario.is_admin)
        
        # Redirigir al inicio
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("registro.html", {
            "request": request,
            "error": f"Error al crear el usuario: {str(e)}",
            "username": username,
            "email": email
        })


@router.get("/logout")
async def logout(request: Request):
    """Cierra la sesión"""
    destruir_sesion(request)
    return RedirectResponse(url="/auth/login", status_code=303)
