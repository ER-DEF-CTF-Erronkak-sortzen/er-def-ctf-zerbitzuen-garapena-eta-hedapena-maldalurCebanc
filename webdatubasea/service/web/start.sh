#!/bin/bash

# Esperar a que el servicio MySQL esté disponible
until mysql -h db -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1" > /dev/null 2>&1; do
    echo "Esperando a que la base de datos MySQL esté disponible..."
    sleep 1
done

# Crear la tabla en la base de datos (si no existe)
echo "Creando la tabla 'usuarios' si no existe..."
mysql -h db -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "
    CREATE DATABASE IF NOT EXISTS faulty_db;
    USE faulty_db;
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"

echo "La base de datos está disponible. Iniciando el servidor web..."
php -S 0.0.0.0:80
