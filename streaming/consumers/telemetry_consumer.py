"""
Kafka consumer for AtmoSync telemetry.
"""

import json
import sys
from pathlib import Path

from kafka import KafkaConsumer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "atmosync-telemetry"


def create_consumer() -> KafkaConsumer:
    """Create and configure the Kafka consumer."""

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="atmosync-live-consumer",
    )


def main() -> None:
    """Read telemetry messages from Kafka."""

    consumer = create_consumer()

    print("AtmoSync Kafka Consumer started.")
    print("Waiting for telemetry...\n")

    try:
        for message in consumer:
            try:
                telemetry = json.loads(
                    message.value.decode("utf-8")
                )

                required_fields = [
                    "timestamp",
                    "container_id",
                    "commodity",
                    "quantity_kg",
                    "origin",
                    "destination",
                    "temperature_c",
                    "humidity_pct",
                    "vibration_g",
                ]

                missing_fields = [
                    field
                    for field in required_fields
                    if field not in telemetry
                ]

                if missing_fields:
                    print(
                        f"Skipping non-telemetry JSON message | "
                        f"offset={message.offset} | "
                        f"missing={missing_fields}"
                    )
                    continue

                print(
                    f"Received telemetry | "
                    f"container={telemetry['container_id']} | "
                    f"commodity={telemetry['commodity']} | "
                    f"temperature={telemetry['temperature_c']}°C | "
                    f"humidity={telemetry['humidity_pct']}% | "
                    f"vibration={telemetry['vibration_g']}g"
                )

            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                print(
                    f"Skipping invalid Kafka message | "
                    f"offset={message.offset} | "
                    f"error={error}"
                )

    except KeyboardInterrupt:
        print("\nAtmoSync Kafka Consumer stopped.")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()