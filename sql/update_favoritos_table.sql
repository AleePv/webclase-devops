-- Script para actualizar tabla de favoritos con comentario y estrellas

USE Alexandra;

-- Agregar columnas comentario y estrellas a la tabla existente
ALTER TABLE usuario_pelicula_favoritos
ADD COLUMN comentario TEXT,
ADD COLUMN estrellas INT DEFAULT 0;

-- Verificar la estructura
DESCRIBE usuario_pelicula_favoritos;