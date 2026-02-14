from domain.model.Pelicula import Pelicula


class PeliculaRepository:
    
    def get_all(self, database):
        """Obtiene todas las películas"""
        cursor = database.cursor()
        cursor.execute("SELECT id, titulo, genero, año, director, imagen_path FROM pelicula")
        peliculas = []
        for (id, titulo, genero, año, director, imagen_path) in cursor:
            peliculas.append(Pelicula(id, titulo, genero, año, director, imagen_path))
        cursor.close()
        return peliculas
    
    def get_by_id(self, database, pelicula_id: int):
        """Obtiene una película por ID"""
        cursor = database.cursor()
        cursor.execute("SELECT id, titulo, genero, año, director, imagen_path FROM pelicula WHERE id = %s", (pelicula_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return Pelicula(result[0], result[1], result[2], result[3], result[4], result[5])
        return None
    
    def insertar_pelicula(self, database, pelicula: Pelicula):
        """Inserta una nueva película"""
        cursor = database.cursor()
        sql = "INSERT INTO pelicula (titulo, genero, año, director, imagen_path) VALUES (%s, %s, %s, %s, %s)"
        valores = (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.imagen_path)
        cursor.execute(sql, valores)
        database.commit()
        cursor.close()
    
    def actualizar_pelicula(self, database, pelicula: Pelicula):
        """Actualiza una película existente"""
        cursor = database.cursor()
        sql = "UPDATE pelicula SET titulo = %s, genero = %s, año = %s, director = %s, imagen_path = %s WHERE id = %s"
        valores = (pelicula.titulo, pelicula.genero, pelicula.año, pelicula.director, pelicula.imagen_path, pelicula.id)
        cursor.execute(sql, valores)
        database.commit()
        cursor.close()
    
    def borrar_pelicula(self, database, pelicula_id: int):
        """Borra una película por ID"""
        # Obtener la película para eliminar la imagen si existe
        pelicula = self.get_by_id(database, pelicula_id)
        if pelicula and pelicula.imagen_path:
            import os
            image_path = os.path.join("static", "images", pelicula.imagen_path)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        cursor = database.cursor()
        cursor.execute("DELETE FROM pelicula WHERE id = %s", (pelicula_id,))
        database.commit()
        cursor.close()
