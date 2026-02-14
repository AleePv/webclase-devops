-- Script para crear tabla de favoritos extendida

USE Alexandra;

-- Crear tabla de favoritos con comentario y estrellas
/*
Esta tabla almacena las películas favoritas de cada usuario.
- usuario_id: ID del usuario (clave foránea a usuarios.id)
- pelicula_id: ID de la película (clave foránea a pelicula.id)
- fecha_agregado: Fecha y hora cuando se agregó a favoritos (automática)
- comentario: Texto opcional del usuario sobre la película
- estrellas: Calificación de 0 a 5 estrellas (por defecto 0)
- PRIMARY KEY: Combinación única de usuario y película (un usuario no puede tener la misma película dos veces)
- FOREIGN KEY: Si se borra un usuario o película, se eliminan sus favoritos automáticamente (CASCADE)
- ENGINE=InnoDB: Motor de base de datos para soporte de transacciones y claves foráneas
- CHARSET=utf8mb4: Soporte para caracteres especiales y emojis
*/
CREATE TABLE IF NOT EXISTS usuario_pelicula_favoritos (
    usuario_id INT NOT NULL,
    pelicula_id INT NOT NULL,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    estrellas INT DEFAULT 0,
    PRIMARY KEY (usuario_id, pelicula_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (pelicula_id) REFERENCES pelicula(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;