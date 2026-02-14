from data.database import database
from data.favoritos_repository import FavoritosRepository

favoritos_repo = FavoritosRepository()
try:
    favoritos = favoritos_repo.get_favoritos_usuario(database, 1)
    print("Favoritos obtenidos:", len(favoritos))
    for fav in favoritos:
        print(f"Pelicula: {fav['pelicula'].titulo}, Estrellas: {fav['estrellas']}, Comentario: {fav['comentario']}")
except Exception as e:
    print(f"Error: {e}")

try:
    todos = favoritos_repo.get_todos_favoritos(database)
    print("Todos los favoritos:", len(todos))
    for fav in todos:
        print(f"Usuario: {fav['username']}, Pelicula: {fav['pelicula'].titulo}, Estrellas: {fav['estrellas']}")
except Exception as e:
    print(f"Error en todos: {e}")