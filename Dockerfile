# Usamos una imagen base ligera de Python
FROM python:3.11-slim

# Instalamos las dependencias del sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de requerimientos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto
COPY . .

# Exponemos el puerto
EXPOSE 5000

# Comando para arrancar la aplicación con Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT app:app
