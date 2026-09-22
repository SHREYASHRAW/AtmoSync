"""
Main entry point for the AtmoSync IoT simulator.
"""

import time

from simulator.config.commodities import get_commodity_profile
from simulator.config.containers import CONTAINER_CONFIG
from simulator.models.telemetry import TelemetryEvent
from simulator.scenarios.climate import ClimateScenario
from simulator.scenarios.state import ScenarioState
from streaming.producers.telemetry_producer import TelemetryProducer


def create_telemetry_event(
    container_id: str,
    commodity: str,
    quantity_kg: float,
    origin: str,
    destination: str,
    scenario: str = "normal",
) -> TelemetryEvent:
    """Create a complete telemetry event for a container."""

    profile = get_commodity_profile(commodity)

    climate = ClimateScenario(**profile)

    if scenario == "normal":
        reading = climate.generate_normal_reading()
    elif scenario == "warning":
        reading = climate.generate_warning_reading()
    elif scenario == "critical":
        reading = climate.generate_critical_reading()
    else:
        raise ValueError(
            "Invalid scenario. Choose: normal, warning, or critical."
        )

    return TelemetryEvent(
        timestamp=TelemetryEvent.current_timestamp(),
        container_id=container_id,
        commodity=commodity,
        quantity_kg=quantity_kg,
        origin=origin,
        destination=destination,
        temperature_c=reading.temperature_c,
        humidity_pct=reading.humidity_pct,
        vibration_g=reading.vibration_g,
    )


def build_containers() -> list[dict]:
    """Build runtime container objects from the configuration."""

    containers = []

    for config in CONTAINER_CONFIG:
        container = {
            "container_id": config["container_id"],
            "commodity": config["commodity"],
            "quantity_kg": config["quantity_kg"],
            "origin": config["origin"],
            "destination": config["destination"],
            "state": ScenarioState(config["initial_state"]),
        }

        containers.append(container)

    return containers


def main() -> None:
    """Continuously generate simulated telemetry."""

    containers = build_containers()
    interval_seconds = 3
    producer = TelemetryProducer()

    print("AtmoSync IoT Simulator started.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            for container in containers:

                scenario = container["state"].get_current_state()

                event = create_telemetry_event(
                    container_id=container["container_id"],
                    commodity=container["commodity"],
                    quantity_kg=container["quantity_kg"],
                    origin=container["origin"],
                    destination=container["destination"],
                    scenario=scenario,
                )

                container["state"].next_state()

                producer.send(event)
        

                print(
                    f"{event.container_id} | "
                    f"{scenario.upper():8} | "
                    f"{event.to_json()}"
                )

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nAtmoSync IoT Simulator stopped.")

    finally:
        producer.close()


if __name__ == "__main__":
    main()