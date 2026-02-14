"""
Dependencias de FastAPI para autenticación
Funcionan como interceptores/filtros
"""
from fastapi import HTTPException, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from utils.session import obtener_usuario_actual

# Inicializar templates
templates = Jinja2Templates(directory="templatesitos")


def require_auth(request: Request):
    """
    Dependencia que requiere autenticación.
    Si el usuario no está autenticado, devuelve RedirectResponse (corta el flujo).
    Si está autenticado, devuelve el usuario.
    
    Uso:
        @app.get("/ruta-protegida")
        async def mi_ruta(usuario: dict = Depends(require_auth)):
            # usuario ya está disponible aquí
            return {"mensaje": f"Hola {usuario['username']}"}
    """
    usuario = obtener_usuario_actual(request)
    print(f"Ejecutando require_auth {usuario}")
    if not usuario:
        print(f"Redireccion a login")
        # Devolver RedirectResponse directamente - FastAPI corta el flujo
        #return RedirectResponse(url="/auth/login", status_code=303)
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/auth/login"}
        )
    return usuario


def require_auth_admin(request: Request):
    """
    Dependencia que requiere autenticación Y rol de administrador.
    Verifica que el usuario esté autenticado y que is_admin sea True.
    
    Uso:
        @app.get("/ruta-admin")
        async def mi_ruta(usuario: dict = Depends(require_auth_admin)):
            # Solo admins pueden llegar aquí
            return {"mensaje": f"Hola admin {usuario['username']}"}
    """
    usuario = obtener_usuario_actual(request)
    print(f"Ejecutando require_auth_admin: {usuario}")
    
    if not usuario:
        print(f"Usuario no autenticado - Redirigiendo a login")
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/auth/login"}
        )
    
    # Verificar que sea administrador usando el campo is_admin
    if not usuario.get("is_admin", False):
        print(f"Usuario {usuario.get('username')} no es admin - Acceso denegado")
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/auth/prohibido"}
        )
    
    return usuario



def optional_auth(request: Request) -> Optional[dict]:
    """
    Dependencia de autenticación opcional.
    No redirige si no está autenticado, solo devuelve None.
    
    Uso:
        @app.get("/ruta-opcional")
        async def mi_ruta(usuario: Optional[dict] = Depends(optional_auth)):
            if usuario:
                return {"mensaje": f"Hola {usuario['username']}"}
            else:
                return {"mensaje": "Hola invitado"}
    """
    return obtener_usuario_actual(request)

def require_role(required_role: str):
    """
    Factory para crear dependencias de roles específicos.
    
    Uso:
        @app.get("/admin")
        async def admin(request: Request, usuario: dict = Depends(require_role("admin"))):
            pass
    
    NOTA: Requiere que el Request sea un parámetro de la ruta para poder renderizar templates.
    """
    def role_checker(request: Request, usuario: dict = Depends(require_auth)) -> dict:
        if usuario.get("role") != required_role:
            # ✅ Devolver TemplateResponse con plantilla 403.html
            return templates.TemplateResponse(
                "403.html",
                {
                    "request": request,
                    "message": f"No tienes permisos suficientes para acceder a esta página.",
                    "required_role": f"Se requiere rol: {required_role}",
                    "current_role": usuario.get("role", "sin rol"),
                    "icon": "🚫"
                },
                status_code=403
            )
        return usuario
    return role_checker


def require_admin(request: Request, usuario: dict = Depends(require_auth)) -> dict:
    """
    Requiere rol de administrador.
    
    Uso:
        @app.get("/admin")
        async def admin(request: Request, usuario: dict = Depends(require_admin)):
            pass
    
    NOTA: Requiere que el Request sea un parámetro de la ruta.
    """
    if usuario.get("role") not in ["admin", "superadmin"]:
        # ✅ Devolver TemplateResponse con plantilla 403.html
        return templates.TemplateResponse(
            "403.html",
            {
                "request": request,
                "message": "Esta página requiere permisos de Administrador.",
                "required_role": "Roles permitidos: admin, superadmin",
                "current_role": usuario.get("role", "sin rol"),
                "icon": "🔒"
            },
            status_code=403
        )
    return usuario


def require_superadmin(request: Request, usuario: dict = Depends(require_auth)) -> dict:
    """
    Requiere rol de super administrador.
    
    Uso:
        @app.get("/superadmin")
        async def superadmin_route(request: Request, usuario: dict = Depends(require_superadmin)):
            pass
    
    NOTA: Requiere que el Request sea un parámetro de la ruta.
    """
    if usuario.get("role") != "superadmin":
        # ✅ Devolver TemplateResponse con plantilla 403.html
        return templates.TemplateResponse(
            "403.html",
            {
                "request": request,
                "message": "Esta página requiere permisos de Super Administrador.",
                "required_role": "Solo el super administrador tiene acceso",
                "current_role": usuario.get("role", "sin rol"),
                "icon": "👑"
            },
            status_code=403
        )
    return usuario


def require_any_role(*roles: str):
    """
    Requiere cualquiera de los roles especificados.
    
    Uso:
        @app.get("/teachers-and-admins")
        async def route(request: Request, usuario = Depends(require_any_role("teacher", "admin"))):
            pass
    
    NOTA: Requiere que el Request sea un parámetro de la ruta.
    """
    def role_checker(request: Request, usuario: dict = Depends(require_auth)) -> dict:
        if usuario.get("role") not in roles:
            # ✅ Devolver TemplateResponse con plantilla 403.html
            roles_text = ", ".join(roles)
            return templates.TemplateResponse(
                "403.html",
                {
                    "request": request,
                    "message": "No tienes permisos suficientes para acceder a esta página.",
                    "required_role": f"Roles permitidos: {roles_text}",
                    "current_role": usuario.get("role", "sin rol"),
                    "icon": "⚠️"
                },
                status_code=403
            )
        return usuario
    return role_checker

# Alias para mayor claridad
get_current_user = require_auth
get_optional_user = optional_auth
