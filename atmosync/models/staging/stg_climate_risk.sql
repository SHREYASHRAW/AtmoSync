{{ config(
    materialized='view'
) }}

WITH telemetry AS (

    SELECT *
    FROM {{ ref('stg_telemetry') }}

),

risk_calculation AS (

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

        CASE
            WHEN commodity = 'avocado'
                THEN 4.0
            WHEN commodity = 'banana'
                THEN 13.0
            WHEN commodity = 'mango'
                THEN 10.0
        END AS temperature_min_c,

        CASE
            WHEN commodity = 'avocado'
                THEN 7.0
            WHEN commodity = 'banana'
                THEN 15.0
            WHEN commodity = 'mango'
                THEN 13.0
        END AS temperature_max_c,

        CASE
            WHEN commodity = 'avocado'
                THEN 65.0
            WHEN commodity = 'banana'
                THEN 85.0
            WHEN commodity = 'mango'
                THEN 85.0
        END AS humidity_min_pct,

        CASE
            WHEN commodity = 'avocado'
                THEN 80.0
            WHEN commodity = 'banana'
                THEN 95.0
            WHEN commodity = 'mango'
                THEN 90.0
        END AS humidity_max_pct

    FROM telemetry

)

SELECT
    *,
    
    CASE
        WHEN temperature_c < temperature_min_c
            THEN temperature_min_c - temperature_c
        WHEN temperature_c > temperature_max_c
            THEN temperature_c - temperature_max_c
        ELSE 0
    END AS temperature_deviation_c,

    CASE
        WHEN humidity_pct < humidity_min_pct
            THEN humidity_min_pct - humidity_pct
        WHEN humidity_pct > humidity_max_pct
            THEN humidity_pct - humidity_max_pct
        ELSE 0
    END AS humidity_deviation_pct,

    CASE
        WHEN temperature_c BETWEEN temperature_min_c AND temperature_max_c
         AND humidity_pct BETWEEN humidity_min_pct AND humidity_max_pct
         AND vibration_g <= 0.20
            THEN 'NORMAL'

        WHEN temperature_c <= temperature_max_c + 3
         AND humidity_pct <= humidity_max_pct + 10
         AND vibration_g <= 0.40
            THEN 'WARNING'

        ELSE 'CRITICAL'
    END AS climate_risk_level

FROM risk_calculation