"""
Commodity environmental profiles for the AtmoSync IoT simulator.

These profiles define the target environmental conditions used by the
simulator to generate realistic telemetry and climate-risk scenarios.
"""

COMMODITY_PROFILES = {
    "avocado": {
        "temperature_min_c": 4.0,
        "temperature_max_c": 7.0,
        "humidity_min_pct": 65.0,
        "humidity_max_pct": 80.0,
    },
    "banana": {
        "temperature_min_c": 13.0,
        "temperature_max_c": 15.0,
        "humidity_min_pct": 85.0,
        "humidity_max_pct": 95.0,
    },
    "mango": {
        "temperature_min_c": 10.0,
        "temperature_max_c": 13.0,
        "humidity_min_pct": 85.0,
        "humidity_max_pct": 90.0,
    },
}


def get_commodity_profile(commodity: str) -> dict:
    """
    Return the environmental profile for a commodity.

    Parameters
    ----------
    commodity : str
        Commodity name, such as 'avocado', 'banana', or 'mango'.

    Returns
    -------
    dict
        Environmental profile for the requested commodity.

    Raises
    ------
    ValueError
        If the commodity is not supported.
    """
    commodity = commodity.lower().strip()

    if commodity not in COMMODITY_PROFILES:
        supported = ", ".join(COMMODITY_PROFILES.keys())
        raise ValueError(
            f"Unsupported commodity '{commodity}'. "
            f"Supported commodities: {supported}"
        )

    return COMMODITY_PROFILES[commodity]