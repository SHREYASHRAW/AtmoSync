"""
Telemetry data model for the AtmoSync IoT simulator.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class TelemetryEvent:
    """Represents one sensor reading from a shipping container."""

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
        """Convert the telemetry event into a dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert the telemetry event into a JSON string."""
        import json

        return json.dumps(self.to_dict())

    @staticmethod
    def current_timestamp() -> str:
        """Return the current UTC timestamp in ISO 8601 format."""
        return datetime.now(timezone.utc).isoformat()