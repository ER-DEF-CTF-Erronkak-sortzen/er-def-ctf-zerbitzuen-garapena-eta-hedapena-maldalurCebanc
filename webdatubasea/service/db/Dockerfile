# Usa una imagen base de MySQL 8.0
FROM mysql:8.0

# Establece la contraseña de root y el nombre de la base de datos
ENV MYSQL_ROOT_PASSWORD='root_password'
ENV MYSQL_DATABASE='faulty_db'
ENV MYSQL_USER='dev1'
ENV MYSQL_PASSWORD='dev1_password'
ENV DB_HOST='db'


# Exponga el puerto 3306 para permitir la conexión a la base de datos
EXPOSE 3306

# Inicia el servicio de MySQL cuando se inicie el contenedor
CMD ["docker-entrypoint.sh", "mysqld"]