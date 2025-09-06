# GDS Kafka Assignment

## 📌 Descripción
Esta app conecta una base de datos **MySQL** con **Confluent Kafka (Confluent Cloud)**.  
El flujo completo:
1. `producer.py` lee cambios incrementales de la tabla `product` y los envía a un **topic Kafka** en formato **Avro**.
2. `consumer.py` escucha el topic, transforma los registros y guarda los resultados en `output.json`.
3. `init_db.py` ejecuta `querys.sql` para crear la base y la tabla si no existen.

---

## 📂 Contenido del repo
- `producer.py` → produce mensajes desde MySQL hacia Kafka.
- `consumer.py` → consume mensajes de Kafka y guarda transformaciones en JSON.
- `init_db.py` → inicializa la base y tabla usando `querys.sql`.
- `querys.sql` → script SQL con `CREATE DATABASE` y `CREATE TABLE`.
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
