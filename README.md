# GDS Kafka Assignment

## 📌 Descripción
Esta app pretende producir datos una base de datos **MySQL** hacia un topic de **Confluent Kafka (Confluent Cloud)** y que estos datos entrantes al topic puedan consumirse.  
El flujo completo:
1. `producer.py` lee cambios incrementales de la tabla `product` y los envía a un **topic Kafka** en formato **Avro**.
2. `consumer.py` escucha el topic, transforma los registros y guarda los resultados en `output.json`.
3. `init_db.py` ejecuta `querys.sql` para crear la base y la tabla si no existen.

---

## 📂 Contenido del repo
- `producer.py` → produce mensajes desde MySQL hacia Kafka.
- `consumer.py` → consume mensajes de Kafka y guarda transformaciones en JSON.
- `init_db.py` → inicializa la base y tabla usando `querys.sql`.
- `querys.sql` → script SQL con `CREATE DATABASE`, `CREATE TABLE` e inserciones de prueba.
- `requirements.txt` → dependencias Python.
- `Dockerfile` → construcción de imagen de la app.
- `docker-compose.yml` → orquestación de servicios.
- `.env.example` → plantilla de configuración de variables de entorno.
- `.gitignore` → evita subir `venv/`, `.env`, etc.

---

## ⚙️ Requisitos
- **Docker + Docker Compose** (recomendado).
- **Python 3.8+** (si lo corres sin Docker).
- Una **instancia de MySQL** local o en contenedor.
- Credenciales de **Confluent Cloud** (Kafka + Schema Registry).

---

## 🔑 Configuración de entorno
1. Copia el archivo `.env.example` como `.env`:
   ```bash
   cp .env.example .env   # Linux / Mac
   Copy-Item .env.example .env   # PowerShell

2. Edita .env con tus credenciales reales:
    ```bash
    # Kafka / Confluent Cloud
    KAFKA_BOOTSTRAP=pkc-xxxxxx.confluent.cloud:9092
    KAFKA_API_KEY=tu_api_key
    KAFKA_API_SECRET=tu_api_secret

    # Schema Registry
    SCHEMA_REGISTRY_URL=https://psrc-xxxxxx.confluent.cloud
    SCHEMA_REGISTRY_KEY=tu_schema_key
    SCHEMA_REGISTRY_SECRET=tu_schema_secret

    # Topic / Schema
    KAFKA_TOPIC=changes_product_table
    SCHEMA_SUBJECT=changes_product_table-value

    # MySQL
    MYSQL_HOST=host.docker.internal   # si usas MySQL local
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=tu_password
    MYSQL_DATABASE=assKafka_BuyOnline_Company

## ¿CÓMO LO PRUEBO?
1. Construir la imagen:
    ```bash
    docker-compose build

2. Levantar la app con 5 consumers:
    ```bash
    docker-compose up --scale consumer=5

3. Parar y limpiar:
    ```bash
    docker-compose down