"""
Climate scenario engine for the AtmoSync IoT simulator.

This module generates realistic environmental conditions for
normal, warning, and critical container states.
"""

import random
from dataclasses import dataclass


@dataclass
class ClimateReading:
    """Represents simulated environmental sensor values."""

    temperature_c: float
    humidity_pct: float
    vibration_g: float


class ClimateScenario:
    """Generate sensor readings based on a climate scenario."""

    def __init__(
        self,
        temperature_min_c: float,
        temperature_max_c: float,
        humidity_min_pct: float,
        humidity_max_pct: float,
    ):
        self.temperature_min_c = temperature_min_c
        self.temperature_max_c = temperature_max_c
        self.humidity_min_pct = humidity_min_pct
        self.humidity_max_pct = humidity_max_pct

    def generate_normal_reading(self) -> ClimateReading:
        """Generate a reading within normal operating conditions."""

        temperature = random.uniform(
            self.temperature_min_c,
            self.temperature_max_c,
        )

        humidity = random.uniform(
            self.humidity_min_pct,
            self.humidity_max_pct,
        )

        vibration = random.uniform(0.05, 0.20)

        return ClimateReading(
            temperature_c=round(temperature, 2),
            humidity_pct=round(humidity, 2),
            vibration_g=round(vibration, 3),
        )

    def generate_warning_reading(self) -> ClimateReading:
        """Generate a reading indicating deteriorating conditions."""

        temperature = random.uniform(
            self.temperature_max_c,
            self.temperature_max_c + 3.0,
        )

        humidity = random.uniform(
            self.humidity_max_pct,
            min(self.humidity_max_pct + 10.0, 100.0),
        )

        vibration = random.uniform(0.20, 0.40)

        return ClimateReading(
            temperature_c=round(temperature, 2),
            humidity_pct=round(humidity, 2),
            vibration_g=round(vibration, 3),
        )

    def generate_critical_reading(self) -> ClimateReading:
        """Generate a reading representing severe conditions."""

        temperature = random.uniform(
            self.temperature_max_c + 3.0,
            self.temperature_max_c + 7.0,
        )

        humidity = random.uniform(
            min(self.humidity_max_pct + 10.0, 100.0),
            100.0,
        )

        vibration = random.uniform(0.40, 0.80)

        return ClimateReading(
            temperature_c=round(temperature, 2),
            humidity_pct=round(humidity, 2),
            vibration_g=round(vibration, 3),
        )