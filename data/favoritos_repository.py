from domain.model.Pelicula import Pelicula


class FavoritosRepository:
    
    def agregar_favorito(self, database, usuario_id: int, pelicula_id: int, comentario: str = "", stars: int = 0):
        """Agrega una película a los favoritos de un usuario con comentario y estrellas"""
        cursor = database.cursor()
        try:
            sql = "INSERT INTO usuario_pelicula_favoritos (usuario_id, pelicula_id, comentario, estrellas) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario_id, pelicula_id, comentario, stars))
            database.commit()
            cursor.close()
            return True
        except Exception as e:
            # Si ya existe, actualizar comentario y estrellas
            cursor.close()
            cursor = database.cursor()
            sql = "UPDATE usuario_pelicula_favoritos SET comentario = %s, estrellas = %s WHERE usuario_id = %s AND pelicula_id = %s"
            cursor.execute(sql, (comentario, stars, usuario_id, pelicula_id))
            database.commit()
            cursor.close()
            return True
    
    def quitar_favorito(self, database, usuario_id: int, pelicula_id: int):
        """Quita una película de los favoritos de un usuario"""
        cursor = database.cursor()
        sql = "DELETE FROM usuario_pelicula_favoritos WHERE usuario_id = %s AND pelicula_id = %s"
        cursor.execute(sql, (usuario_id, pelicula_id))
        database.commit()
        cursor.close()
    
    def es_favorito(self, database, usuario_id: int, pelicula_id: int) -> bool:
        """Verifica si una película es favorita de un usuario"""
        cursor = database.cursor()
        sql = "SELECT COUNT(*) FROM usuario_pelicula_favoritos WHERE usuario_id = %s AND pelicula_id = %s"
        cursor.execute(sql, (usuario_id, pelicula_id))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    
    def get_favoritos_ids_usuario(self, database, usuario_id: int):
        """Obtiene los IDs de las películas favoritas de un usuario"""
        cursor = database.cursor()
        sql = "SELECT pelicula_id FROM usuario_pelicula_favoritos WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        ids = [row[0] for row in cursor]
        cursor.close()
        return ids
    
    def get_favoritos_usuario(self, database, usuario_id: int):
        """Obtiene todas las películas favoritas de un usuario"""
        cursor = database.cursor()
        sql = "SELECT p.id, p.titulo, p.genero, p.año, p.director, f.fecha_agregado, f.comentario, f.estrellas FROM pelicula p INNER JOIN usuario_pelicula_favoritos f ON p.id = f.pelicula_id WHERE f.usuario_id = %s ORDER BY f.fecha_agregado DESC"
        cursor.execute(sql, (usuario_id,))
        peliculas_con_fecha = []
        for (id, titulo, genero, año, director, fecha_agregado, comentario, estrellas) in cursor:
            pelicula = Pelicula(id, titulo, genero, año, director)
            peliculas_con_fecha.append({
                'pelicula': pelicula,
                'fecha_agregado': fecha_agregado,
                'comentario': comentario,
                'estrellas': estrellas
            })
        cursor.close()
        return peliculas_con_fecha
    
    def get_todos_favoritos(self, database):
        """Obtiene todos los favoritos de todos los usuarios (solo admin)"""
        cursor = database.cursor()
        sql = "SELECT u.username, p.id, p.titulo, p.genero, p.año, p.director, f.fecha_agregado, f.comentario, f.estrellas FROM usuario_pelicula_favoritos f INNER JOIN usuarios u ON f.usuario_id = u.id INNER JOIN pelicula p ON f.pelicula_id = p.id ORDER BY f.fecha_agregado DESC"
        cursor.execute(sql)
        favoritos = []
        for (username, id, titulo, genero, año, director, fecha_agregado, comentario, estrellas) in cursor:
            pelicula = Pelicula(id, titulo, genero, año, director)
            favoritos.append({
                'username': username,
                'pelicula': pelicula,
                'fecha_agregado': fecha_agregado,
                'comentario': comentario,
                'estrellas': estrellas
            })
        cursor.close()
        return favoritos
    
    def actualizar_favorito(self, database, usuario_id: int, pelicula_id: int, comentario: str, stars: int):
        """Actualiza el comentario y estrellas de un favorito"""
        cursor = database.cursor()
        sql = "UPDATE usuario_pelicula_favoritos SET comentario = %s, estrellas = %s WHERE usuario_id = %s AND pelicula_id = %s"
        cursor.execute(sql, (comentario, stars, usuario_id, pelicula_id))
        database.commit()
        cursor.close()
        return True
