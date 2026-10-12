"""
Container configuration for the AtmoSync IoT simulator.

This module defines the containers that will be monitored
by the simulated IoT system.
"""

CONTAINER_CONFIG = [
    {
        "container_id": "C001",
        "commodity": "avocado",
        "quantity_kg": 5000,
        "origin": "Kenya",
        "destination": "Mumbai",
        "initial_state": "normal",
    },
    {
        "container_id": "C002",
        "commodity": "banana",
        "quantity_kg": 4500,
        "origin": "Ecuador",
        "destination": "Delhi",
        "initial_state": "normal",
    },
    {
        "container_id": "C003",
        "commodity": "mango",
        "quantity_kg": 4000,
        "origin": "India",
        "destination": "Pune",
        "initial_state": "warning",
    },
]