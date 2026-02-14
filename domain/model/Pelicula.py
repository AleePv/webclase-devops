class Pelicula:
    def __init__(self, id: int, titulo: str, genero: str, año: int, director: str, imagen_path: str = None):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.año = año
        self.director = director
        self.imagen_path = imagen_path

    def __str__(self):
        return f"Pelicula(id={self.id}, titulo='{self.titulo}', genero='{self.genero}', año={self.año}, director='{self.director}', imagen_path='{self.imagen_path}')"
