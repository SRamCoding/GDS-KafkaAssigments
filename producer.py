import os
import time
import mysql.connector
from dotenv import load_dotenv
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

# Cargar .env si corres localmente (no afecta a Docker)
load_dotenv()


def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed for record {msg.key()}: {err}")
    else:
        print(
            f"✅ Record {msg.key()} produced to {msg.topic()} "
            f"[{msg.partition()}] at offset {msg.offset()}"
        )


# ---------- Kafka + Schema Registry Configuration ----------
kafka_config = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP"),
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET"),
}

schema_registry_client = SchemaRegistryClient({
    'url': os.getenv("SCHEMA_REGISTRY_URL"),
    'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_KEY')}:{os.getenv('SCHEMA_REGISTRY_SECRET')}"
})

# Topic y Subject dinámicos
topic_name = os.getenv("KAFKA_TOPIC", "product_updates")
subject_name = os.getenv("SCHEMA_SUBJECT", "product_updates-value")

# Obtener Avro schema
schema_str = schema_registry_client.get_latest_version(subject_name).schema.schema_str
key_serializer = StringSerializer('utf_8')
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

# Producer
producer_conf = {
    **kafka_config,
    'key.serializer': key_serializer,
    'value.serializer': avro_serializer
}
producer = SerializingProducer(producer_conf)


# ---------- MySQL Connection ----------
mysql_conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", "rootpass"),
    database=os.getenv("MYSQL_DATABASE", "assKafka_BuyOnline_Company")
)
cursor = mysql_conn.cursor(dictionary=True)


# ---------- Incremental Fetch ----------
last_read_timestamp = "1970-01-01 00:00:00"

def fetch_incremental_data():
    global last_read_timestamp
    query = f"""
        SELECT * FROM product
        WHERE last_updated > '{last_read_timestamp}'
        ORDER BY last_updated ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        last_read_timestamp = rows[-1]["last_updated"].strftime("%Y-%m-%d %H:%M:%S")
    return rows


# ---------- Main Loop con manejo bonito ----------
try:
    while True:
        records = fetch_incremental_data()
        for row in records:
            product = {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "last_updated": str(row["last_updated"])
            }

            producer.produce(
                topic=topic_name,
                key=str(product["id"]),
                value=product,
                on_delivery=delivery_report
            )
            print(f"🚀 Produced: {product}")

        producer.flush()
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Producer detenido por el usuario.")

finally:
    producer.flush()
    cursor.close()
    mysql_conn.close()
    print("✅ Conexión MySQL cerrada y producer apagado correctamente.")