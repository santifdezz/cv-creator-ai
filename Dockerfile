FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para ReportLab
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para archivos temporales
RUN mkdir -p /tmp/cv_generator

# Exponer el puerto
EXPOSE 7860

# Variables de entorno
ENV PYTHONPATH=/app
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]