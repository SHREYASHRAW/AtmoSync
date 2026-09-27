{{ config(
    materialized='view'
) }}

WITH exposure_data AS (

    SELECT *
    FROM {{ ref('stg_exposure') }}

)

SELECT
    container_id,
    commodity,
    quantity_kg,
    origin,
    destination,

    COUNT(*) AS total_readings,

    SUM(
        CASE
            WHEN climate_risk_level = 'NORMAL' THEN 1
            ELSE 0
        END
    ) AS normal_readings,

    SUM(
        CASE
            WHEN climate_risk_level = 'WARNING' THEN 1
            ELSE 0
        END
    ) AS warning_readings,

    SUM(
        CASE
            WHEN climate_risk_level = 'CRITICAL' THEN 1
            ELSE 0
        END
    ) AS critical_readings,

    ROUND(
        SUM(
            CASE
                WHEN climate_risk_level = 'WARNING'
                    THEN exposure_interval_minutes
                ELSE 0
            END
        ),
        2
    ) AS warning_exposure_minutes,

    ROUND(
        SUM(
            CASE
                WHEN climate_risk_level = 'CRITICAL'
                    THEN exposure_interval_minutes
                ELSE 0
            END
        ),
        2
    ) AS critical_exposure_minutes,

    ROUND(
        SUM(exposure_interval_minutes),
        2
    ) AS total_exposure_minutes,

    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,

    ROUND(AVG(humidity_pct), 2) AS avg_humidity_pct,

    ROUND(MAX(temperature_c), 2) AS max_temperature_c,

    ROUND(MAX(humidity_pct), 2) AS max_humidity_pct,

    ROUND(MAX(vibration_g), 3) AS max_vibration_g

FROM exposure_data

GROUP BY
    container_id,
    commodity,
    quantity_kg,
    origin,
    destination