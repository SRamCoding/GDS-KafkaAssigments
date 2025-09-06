import os
import json
from dotenv import load_dotenv
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

# Cargar .env si corres localmente
load_dotenv()

# ---------- Kafka Configuration ----------
kafka_config = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP"),
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': os.getenv("KAFKA_API_KEY"),
    'sasl.password': os.getenv("KAFKA_API_SECRET"),
    'group.id': os.getenv("KAFKA_GROUP_ID", "group1"),
    'auto.offset.reset': os.getenv("KAFKA_OFFSET_RESET", "earliest"),
}

# ---------- Schema Registry Client ----------
schema_registry_client = SchemaRegistryClient({
    'url': os.getenv("SCHEMA_REGISTRY_URL"),
    'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_KEY')}:{os.getenv('SCHEMA_REGISTRY_SECRET')}"
})

# Obtener el Avro schema
subject_name = os.getenv("SCHEMA_SUBJECT", "product_updates-value")
schema_str = schema_registry_client.get_latest_version(subject_name).schema.schema_str

# ---------- Deserializers ----------
key_deserializer = StringDeserializer('utf_8')
avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

# ---------- Kafka Consumer ----------
consumer_conf = {
    'bootstrap.servers': kafka_config['bootstrap.servers'],
    'security.protocol': kafka_config['security.protocol'],
    'sasl.mechanisms': kafka_config['sasl.mechanisms'],
    'sasl.username': kafka_config['sasl.username'],
    'sasl.password': kafka_config['sasl.password'],
    'key.deserializer': key_deserializer,
    'value.deserializer': avro_deserializer,
    'group.id': kafka_config['group.id'],
    'auto.offset.reset': kafka_config['auto.offset.reset'],
}
consumer = DeserializingConsumer(consumer_conf)

# Suscribirse al topic dinámico
topic_name = os.getenv("KAFKA_TOPIC", "product_updates")
consumer.subscribe([topic_name])


# ---------- Transformación ----------
def transform(record: dict) -> dict:
    if not record:
        return {}
    record["category"] = record["category"].upper()
    if record["category"] == "ELECTRONICS":
        record["price"] = round(record["price"] * 0.9, 2)
    return record


# ---------- Main Loop ----------
try:
    with open("output.json", "a") as f:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"❌ Consumer error: {msg.error()}")
                continue

            key = msg.key()
            value = msg.value()

            record = transform(value)

            f.write(json.dumps(record) + "\n")
            f.flush()

            print(f"✅ Consumed record with key={key}, value={record}")

except KeyboardInterrupt:
    print("🛑 Closing consumer...")
finally:
    consumer.close()
