{{ config(
    materialized='view'
) }}

SELECT
    event_id,
    schema_version,
    timestamp,
    container_id,
    commodity,
    quantity_kg,
    origin,
    destination,
    temperature_c,
    humidity_pct,
    vibration_g

FROM ATMOSYNC.RAW.TELEMETRY