"""
Kafka producer for AtmoSync telemetry.
"""

import json
import sys
from pathlib import Path

from kafka import KafkaProducer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simulator.models.telemetry import TelemetryEvent

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "atmosync-telemetry"


class TelemetryProducer:
    """Send AtmoSync telemetry events to Kafka."""

    def __init__(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def send(self, event: TelemetryEvent) -> None:
        """Send one telemetry event to Kafka."""

        future = self.producer.send(
            KAFKA_TOPIC,
            value=event.to_dict(),
        )

        future.get(timeout=10)

        print(
            f"Sent telemetry | "
            f"container={event.container_id} | "
            f"commodity={event.commodity}"
        )

    def close(self) -> None:
        """Close the Kafka producer."""

        self.producer.close()


if __name__ == "__main__":
    test_event = TelemetryEvent(
        timestamp=TelemetryEvent.current_timestamp(),
        container_id="C001",
        commodity="avocado",
        quantity_kg=5000,
        origin="Kenya",
        destination="Mumbai",
        temperature_c=6.4,
        humidity_pct=78.2,
        vibration_g=0.12,
    )

    producer = TelemetryProducer()

    try:
        producer.send(test_event)
    finally:
        producer.close()