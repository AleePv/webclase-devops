"""
Helpers para generar respuestas de error bonitas
"""
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templatesitos")


def forbidden_response(mensaje: str = "No tienes permisos para acceder a este recurso", 
                       rol_requerido: str = None) -> HTMLResponse:
    """
    Genera una respuesta HTML 403 (Forbidden) bonita
    
    Args:
        mensaje: Mensaje de error personalizado
        rol_requerido: Rol específico requerido (opcional)
    
    Returns:
        HTMLResponse con código 403
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Acceso Denegado - 403</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .error-container {{
                background: white;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 600px;
                animation: slideIn 0.5s ease-out;
            }}
            
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .error-icon {{
                font-size: 100px;
                margin-bottom: 20px;
            }}
            
            h1 {{
                color: #e74c3c;
                font-size: 2.5em;
                margin-bottom: 20px;
            }}
            
            .error-code {{
                color: #95a5a6;
                font-size: 1.2em;
                margin-bottom: 20px;
                font-weight: bold;
            }}
            
            .error-message {{
                color: #555;
                font-size: 1.1em;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            
            .required-role {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #e74c3c;
            }}
            
            .required-role strong {{
                color: #e74c3c;
            }}
            
            .actions {{
                margin-top: 30px;
                display: flex;
                gap: 10px;
                justify-content: center;
                flex-wrap: wrap;
            }}
            
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s;
                font-size: 1em;
            }}
            
            .btn-primary {{
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .btn-secondary {{
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }}
            
            .btn-secondary:hover {{
                background: #667eea;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">🚫</div>
            <h1>Acceso Denegado</h1>
            <div class="error-code">HTTP 403 - Forbidden</div>
            
            <p class="error-message">{mensaje}</p>
            
            {f'<div class="required-role"><strong>🔐 Rol requerido:</strong> {rol_requerido}</div>' if rol_requerido else ''}
            
            <div class="actions">
                <a href="/" class="btn btn-primary">🏠 Volver al Inicio</a>
                <a href="javascript:history.back()" class="btn btn-secondary">← Página Anterior</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content, status_code=403)


def unauthorized_response(mensaje: str = "Debes iniciar sesión para acceder a este recurso") -> HTMLResponse:
    """
    Genera una respuesta HTML 401 (Unauthorized) bonita
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>No Autorizado - 401</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .error-container {{
                background: white;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 600px;
            }}
            
            .error-icon {{
                font-size: 100px;
                margin-bottom: 20px;
            }}
            
            h1 {{
                color: #f39c12;
                font-size: 2.5em;
                margin-bottom: 20px;
            }}
            
            p {{
                color: #555;
                font-size: 1.1em;
                line-height: 1.6;
                margin-bottom: 30px;
            }}
            
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">🔐</div>
            <h1>No Autorizado</h1>
            <p>{mensaje}</p>
            <a href="/auth/login" class="btn">Iniciar Sesión</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content, status_code=401)
