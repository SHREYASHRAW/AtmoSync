"""
Main entry point for the AtmoSync IoT simulator.

This module generates simulated telemetry for configured
shipping containers and publishes the events to Kafka.
"""

import time

from simulator.config.commodities import get_commodity_profile
from simulator.config.containers import CONTAINER_CONFIG
from simulator.models.telemetry import TelemetryEvent
from simulator.scenarios.climate import ClimateScenario
from simulator.scenarios.state import ScenarioState
from simulator.models.telemetry import SCHEMA_VERSION, TelemetryEvent


def create_telemetry_event(
    container_id: str,
    commodity: str,
    quantity_kg: float,
    origin: str,
    destination: str,
    scenario: str,
) -> TelemetryEvent:
    """Create one telemetry event for a container."""

    profile = get_commodity_profile(commodity)

    climate = ClimateScenario(
        temperature_min_c=profile["temperature_min_c"],
        temperature_max_c=profile["temperature_max_c"],
        humidity_min_pct=profile["humidity_min_pct"],
        humidity_max_pct=profile["humidity_max_pct"],
    )

    if scenario == "normal":
        reading = climate.generate_normal_reading()
    elif scenario == "warning":
        reading = climate.generate_warning_reading()
    elif scenario == "critical":
        reading = climate.generate_critical_reading()
    else:
        raise ValueError(f"Unsupported scenario: {scenario}")

    timestamp = TelemetryEvent.current_timestamp()

    event_id = TelemetryEvent.generate_event_id(
        container_id=container_id,
        timestamp=timestamp,
    )

    return TelemetryEvent(
        event_id=event_id,
        schema_version=SCHEMA_VERSION,
        timestamp=timestamp,
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
    """Build runtime state for all configured containers."""

    containers = []

    for config in CONTAINER_CONFIG:
        containers.append(
            {
                **config,
                "state": ScenarioState(
                    initial_state=config["initial_state"]
                ),
            }
        )

    return containers


def main() -> None:
    """Continuously generate and publish simulated telemetry."""

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