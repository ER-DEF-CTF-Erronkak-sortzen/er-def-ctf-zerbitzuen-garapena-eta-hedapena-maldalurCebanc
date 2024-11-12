#!/bin/bash

# Espera hasta que MySQL esté disponible
until mysql -h "$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" 2>/dev/null; do
  echo "Esperando a que la base de datos MySQL esté disponible..."
  sleep 5
done

# Inicia el servidor PHP en el puerto 80
php -S 0.0.0.0:80
