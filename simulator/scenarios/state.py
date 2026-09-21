"""
Scenario state manager for the AtmoSync IoT simulator.

This module controls transitions between normal, warning,
and critical climate states for each container.
"""

import random


class ScenarioState:
    """Manage the current climate state of a container."""

    VALID_STATES = ["normal", "warning", "critical"]

    def __init__(self, initial_state: str = "normal"):
        if initial_state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid initial state '{initial_state}'. "
                f"Choose: {', '.join(self.VALID_STATES)}"
            )

        self.current_state = initial_state

    def get_current_state(self) -> str:
        """Return the current climate state."""
        return self.current_state

    def next_state(self) -> str:
        """Determine and return the next climate state."""

        if self.current_state == "normal":
            transition = random.choices(
                ["normal", "warning"],
                weights=[0.75, 0.25],
            )[0]

        elif self.current_state == "warning":
            transition = random.choices(
                ["normal", "warning", "critical"],
                weights=[0.25, 0.50, 0.25],
            )[0]

        else:
            transition = random.choices(
                ["warning", "critical"],
                weights=[0.60, 0.40],
            )[0]

        self.current_state = transition

        return self.current_state