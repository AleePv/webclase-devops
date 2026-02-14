from domain.model.Usuario import Usuario
import bcrypt


class UsuarioRepository:

    def get_by_username(self, db, username: str) -> Usuario:
        """Obtiene un usuario por su nombre de usuario"""
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, email, is_admin FROM usuarios WHERE username = %s", (username,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4])
        return None

    def get_by_id(self, db, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID"""
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, email, is_admin FROM usuarios WHERE id = %s", (user_id,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4])
        return None

    def get_all(self, db) -> list[Usuario]:
        """Obtiene todos los usuarios"""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios_en_db = cursor.fetchall()
        usuarios: list[Usuario] = list()
        
        for usuario in usuarios_en_db:
            usuario_obj = Usuario(usuario[0], usuario[1], usuario[2], usuario[3])
            usuarios.append(usuario_obj)
        cursor.close()
        
        return usuarios

    def insertar_usuario(self, db, username: str, password: str, email: str = None, is_admin: bool = False) -> None:
        """Inserta un nuevo usuario con contraseña hasheada"""
        cursor = db.cursor()
        
        # Hashear la contraseña con bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, email, is_admin) VALUES (%s, %s, %s, %s)",
            (username, password_hash, email, is_admin)
        )
        
        db.commit()
        cursor.close()

    def verificar_password(self, password: str, password_hash: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        # # Convertir password_hash a bytes si es necesario
        # if isinstance(password_hash, str):
        #     password_hash = password_hash.encode('utf-8')
        # elif isinstance(password_hash, bytearray):
        #     password_hash = bytes(password_hash)
        
        return bcrypt.checkpw(password.encode('utf-8'), bytes(password_hash))

    def actualizar_password(self, db, user_id: int, nueva_password: str) -> None:
        """Actualiza la contraseña de un usuario"""
        cursor = db.cursor()
        
        # Hashear la nueva contraseña
        password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "UPDATE usuarios SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )
        
        db.commit()
        cursor.close()
