"""
Sistema de sesiones avanzado con protección contra Session Hijacking
Similar a lo que hace Google
"""
from fastapi import Request
from typing import Optional
import hashlib


def crear_sesion_segura(request: Request, user_id: int, username: str):
    """Crea una sesión vinculada al dispositivo del usuario"""
    # Obtener información del cliente
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Crear un fingerprint del dispositivo
    device_fingerprint = hashlib.sha256(f"{ip}{user_agent}".encode()).hexdigest()[:16]
    
    # Guardar en la sesión
    request.session["user_id"] = user_id
    request.session["username"] = username
    request.session["authenticated"] = True
    request.session["device_fingerprint"] = device_fingerprint
    request.session["ip"] = ip


def verificar_sesion_segura(request: Request) -> Optional[dict]:
    """Verifica que la sesión sea del mismo dispositivo"""
    if not request.session or not request.session.get("authenticated"):
        return None
    
    # Verificar fingerprint
    ip_actual = request.client.host
    user_agent_actual = request.headers.get("user-agent", "")
    fingerprint_actual = hashlib.sha256(f"{ip_actual}{user_agent_actual}".encode()).hexdigest()[:16]
    
    fingerprint_sesion = request.session.get("device_fingerprint")
    
    # Si el fingerprint no coincide → Posible Session Hijacking
    if fingerprint_actual != fingerprint_sesion:
        # Destruir la sesión sospechosa
        request.session.clear()
        return None
    
    return {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username")
    }


def verificar_cambio_ip(request: Request) -> bool:
    """Detecta si la IP cambió (como Google)"""
    ip_actual = request.client.host
    ip_sesion = request.session.get("ip")
    
    if ip_actual != ip_sesion:
        # IP cambió → Alerta de seguridad
        return True
    
    return False
