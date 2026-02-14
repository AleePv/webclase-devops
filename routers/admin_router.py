"""
Ejemplo de router completamente protegido usando Dependencies
TODAS las rutas de este router requieren autenticación
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.dependencies import require_auth

# Crear router con dependencia global
router = APIRouter(
    prefix="/admin",
    tags=["administración"],
    dependencies=[Depends(require_auth)]  # ✅ Protege TODAS las rutas
)

templates = Jinja2Templates(directory="templatesitos")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Panel de administración
    NO necesita 'usuario = Depends(require_auth)' porque ya está en el router
    """
    # El usuario ya está autenticado por la dependencia del router
    # Si quieres acceder a los datos del usuario, agrégalo:
    # async def dashboard(request: Request, usuario: dict = Depends(require_auth)):
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request
    })


@router.get("/users")
async def list_users():
    """
    Lista de usuarios
    Protegida automáticamente
    """
    return {"users": ["user1", "user2", "user3"]}


@router.get("/stats")
async def statistics():
    """
    Estadísticas
    También protegida
    """
    return {
        "total_users": 150,
        "active_sessions": 42,
        "total_alumnos": 300
    }


# Para usar este router en main.py:
# app.include_router(admin_router.router)
