# Usa una imagen de Python
FROM python:3.8-slim

# Instala Flask
RUN pip install flask

# Copia los archivos de la aplicación
COPY app.py /app/app.py
COPY templates /app/templates

# Define el directorio de trabajo
WORKDIR /app

# Expone el puerto 5000
EXPOSE 5000

# Ejecuta la aplicación
CMD ["python", "app.py"]
