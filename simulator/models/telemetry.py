"""
Telemetry data model for the AtmoSync IoT simulator.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json


SCHEMA_VERSION = "1.0"


@dataclass
class TelemetryEvent:
    """Represents one sensor reading from a shipping container."""

    event_id: str
    schema_version: str
    timestamp: str
    container_id: str
    commodity: str
    quantity_kg: float
    origin: str
    destination: str
    temperature_c: float
    humidity_pct: float
    vibration_g: float

    def to_dict(self) -> dict:
        """Convert the telemetry event to a dictionary."""

        return asdict(self)

    def to_json(self) -> str:
        """Convert the telemetry event to a JSON string."""

        return json.dumps(self.to_dict())

    @staticmethod
    def current_timestamp() -> str:
        """Return the current UTC timestamp."""

        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def generate_event_id(
        container_id: str,
        timestamp: str,
    ) -> str:
        """Generate a unique identifier for a telemetry event."""

        normalized_timestamp = (
            timestamp.replace("-", "")
            .replace(":", "")
            .replace(".", "")
            .replace("+00:00", "Z")
        )

        return f"{container_id}-{normalized_timestamp}"