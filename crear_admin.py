"""
Script para crear un usuario administrador inicial
Ejecutar con: python crear_admin.py
"""
from data.database import database
from data.usuario_repository import UsuarioRepository


def crear_usuario_admin():
    """Crea el usuario administrador si no existe"""
    usuario_repo = UsuarioRepository()
    
    # Verificar si ya existe un admin
    admin_existente = usuario_repo.get_by_username(database, "admin")
    
    if admin_existente:
        print("❌ El usuario 'admin' ya existe en la base de datos")
        print(f"   ID: {admin_existente.id}")
        print(f"   Username: {admin_existente.username}")
        print(f"   Email: {admin_existente.email}")
        print(f"   Es Admin: {admin_existente.is_admin}")
        return
    
    # Datos del administrador
    username = "admin"
    password = "admin123"  # Cambiar después del primer login
    email = "admin@peliculas.com"
    
    try:
        # Crear el usuario administrador
        usuario_repo.insertar_usuario(
            database, 
            username=username, 
            password=password, 
            email=email, 
            is_admin=True  # ⭐ IMPORTANTE: Marcar como administrador
        )
        
        print("✅ Usuario administrador creado exitosamente!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Email: {email}")
        print(f"   Es Admin: True")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
    except Exception as e:
        print(f"❌ Error al crear el usuario administrador: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("CREAR USUARIO ADMINISTRADOR INICIAL")
    print("=" * 60)
    print()
    
    crear_usuario_admin()
    
    print()
    print("=" * 60)
