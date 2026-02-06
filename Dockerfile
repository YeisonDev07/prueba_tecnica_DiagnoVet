# Dockerfile para Cloud Run
# Define cómo empaquetar la aplicación en un contenedor

# Imagen base: Python 3.11 slim (versión ligera)
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app ./app

# Crear directorios necesarios
RUN mkdir -p uploads extracted_images

# Exponer puerto 8080 (Cloud Run lo requiere)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
