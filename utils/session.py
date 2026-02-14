from fastapi import Request
from typing import Optional

# Clave secreta para firmar las cookies de sesión
SECRET_KEY = "tu_clave_secreta_muy_segura_cambiala_en_produccion"


def crear_sesion(request: Request, user_id: int, username: str, is_admin: bool = False):
    """Crea una sesión guardando los datos en request.session"""
    request.session["user_id"] = user_id
    request.session["username"] = username
    request.session["is_admin"] = is_admin
    request.session["authenticated"] = True
    # para logout
    #request.session.popitem("username", None)  # Elimina si existe


def obtener_sesion(request: Request) -> Optional[dict]:
    """Obtiene los datos de la sesión"""
    if not request.session or not request.session.get("authenticated"):
        return None
    
    return {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username"),
        "is_admin": request.session.get("is_admin", False)
    }


def destruir_sesion(request: Request):
    """Destruye la sesión limpiando los datos"""
    request.session.clear()


def usuario_autenticado(request: Request) -> bool:
    """Verifica si hay un usuario autenticado"""
    sesion = obtener_sesion(request)
    return sesion is not None


def obtener_usuario_actual(request: Request) -> Optional[dict]:
    """Obtiene el usuario actual de la sesión"""
    return obtener_sesion(request)
