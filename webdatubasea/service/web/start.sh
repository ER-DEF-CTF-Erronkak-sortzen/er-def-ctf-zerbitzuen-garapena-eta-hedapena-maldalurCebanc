#!/bin/bash

# Esperar a que el servicio MySQL esté disponible
until mysql -h db -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" > /dev/null 2>&1; do
    echo "Esperando a que la base de datos MySQL esté disponible..."
    sleep 1
done

# Crear la base de datos 'faulty_db' si no existe
echo "Creando la db 'faulty_db' si no existe..."
mysql -h db -u root -proot_password -e "
    CREATE DATABASE IF NOT EXISTS faulty_db;
"

# Otorgar privilegios al usuario 'dev1'
echo "Otorgando privilegios a 'dev1'..."
mysql -h db -u root -proot_password -e "
    GRANT CREATE USER, GRANT OPTION, RELOAD ON *.* TO 'dev1'@'%' WITH GRANT OPTION;
    GRANT SELECT, INSERT, UPDATE, DELETE ON faulty_db.* TO 'dev1'@'%';
    FLUSH PRIVILEGES;
"

# Crear la tabla 'usuarios' en 'faulty_db' si no existe
echo "Creando la tabla 'usuarios' si no existe..."
mysql -h db -u "$DB_USER" -p"$DB_PASSWORD" -e "
    USE faulty_db;
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"

# Crear la tabla 'flags' en 'faulty_db' si no existe
echo "Creando la tabla 'flags' si no existe..."
mysql -h db -u "$DB_USER" -p"$DB_PASSWORD" -e "
    USE faulty_db;
    CREATE TABLE IF NOT EXISTS flags (
        id INT AUTO_INCREMENT PRIMARY KEY,
        flag VARCHAR(255) NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"

# Create the dev1 user if it doesn't exist
useradd -m dev1

# Set a root password (Optional)
echo 'dev1:dev1_password' | chpasswd

# Ensure SSH server is running
echo "Iniciando el servidor SSH..."
service ssh start

# Start PHP's built-in web server
echo "Iniciando el servidor web..."
php -S 0.0.0.0:80