{{ config(
    materialized='view'
) }}

WITH risk_data AS (

    SELECT
        *
    FROM {{ ref('stg_climate_risk') }}

),

exposure_calculation AS (

    SELECT
        *,
        
        LAG(timestamp) OVER (
            PARTITION BY container_id
            ORDER BY timestamp
        ) AS previous_timestamp,

        DATEDIFF(
            'second',
            LAG(timestamp) OVER (
                PARTITION BY container_id
                ORDER BY timestamp
            ),
            timestamp
        ) AS seconds_since_previous_reading

    FROM risk_data

)

SELECT
    event_id,
    timestamp,
    container_id,
    commodity,
    quantity_kg,
    origin,
    destination,
    temperature_c,
    humidity_pct,
    vibration_g,

    temperature_deviation_c,
    humidity_deviation_pct,
    climate_risk_level,

    previous_timestamp,

    COALESCE(
        seconds_since_previous_reading,
        0
    ) AS seconds_since_previous_reading,

    ROUND(
        COALESCE(seconds_since_previous_reading, 0) / 60.0,
        2
    ) AS exposure_interval_minutes

FROM exposure_calculation