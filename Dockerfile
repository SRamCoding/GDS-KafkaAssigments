# Imagen base con Python
FROM python:3.11-slim

# Instalar compiladores y librdkafka (necesarios para confluent-kafka)
RUN apt-get update && apt-get install -y \
    gcc g++ librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando por defecto: inicializa la DB y arranca el producer
CMD ["sh", "-c", "python init_db.py && python producer.py"]