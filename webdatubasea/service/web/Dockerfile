# Usa una imagen base de PHP 8
FROM php:8-fpm

# Instala las dependencias necesarias, incluyendo el cliente de MySQL
RUN apt-get update && apt-get install -y \
    libmcrypt-dev \
    libssl-dev \
    build-essential \
    zip \
    default-mysql-client

# Configura la variable de entorno para el directorio de trabajo
WORKDIR /var/www/html

# Copia los archivos del directorio de trabajo a la imagen
COPY . /var/www/html/

# Copia el script de inicialización
COPY start.sh /start.sh

# Inicializa el servidor web
EXPOSE 80

# Configura el comando de inicialización
CMD ["sh", "/start.sh"]