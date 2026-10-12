{{ config(
    materialized='view'
) }}

WITH climate_summary AS (

    SELECT *
    FROM {{ ref('container_climate_summary') }}

),

severity AS (

    SELECT
        *,
        
        /*
        Temperature severity:
        Measures how far the average temperature moved
        outside the commodity's preferred range.
        */

        CASE
            WHEN commodity = 'avocado' THEN
                GREATEST(avg_temperature_c - 7.0, 0)

            WHEN commodity = 'banana' THEN
                GREATEST(avg_temperature_c - 15.0, 0)

            WHEN commodity = 'mango' THEN
                GREATEST(avg_temperature_c - 13.0, 0)

            ELSE 0
        END AS temperature_severity,

        /*
        Humidity severity:
        Measures how far the average humidity moved
        above the commodity's preferred maximum.
        */

        CASE
            WHEN commodity = 'avocado' THEN
                GREATEST(avg_humidity_pct - 80.0, 0)

            WHEN commodity = 'banana' THEN
                GREATEST(avg_humidity_pct - 95.0, 0)

            WHEN commodity = 'mango' THEN
                GREATEST(avg_humidity_pct - 90.0, 0)

            ELSE 0
        END AS humidity_severity

    FROM climate_summary

),

spoilage_calculation AS (

    SELECT
        *,

        /*
        Simulation-based spoilage estimate.

        Critical exposure is weighted more heavily than
        warning exposure because critical conditions
        represent more severe environmental stress.

        The result is capped at 25%.
        This is an analytical simulation assumption,
        not a scientifically validated spoilage model.
        */

        LEAST(
            25.0,

            (
                warning_exposure_minutes * 2.0
            )
            +
            (
                critical_exposure_minutes * 5.0
            )
            +
            (
                temperature_severity * 0.50
            )
            +
            (
                humidity_severity * 0.10
            )
            +
            (
                max_vibration_g * 2.0
            )
        ) AS estimated_spoilage_pct

    FROM severity

)

SELECT
    container_id,
    commodity,
    quantity_kg,
    origin,
    destination,

    total_readings,
    normal_readings,
    warning_readings,
    critical_readings,

    warning_exposure_minutes,
    critical_exposure_minutes,
    total_exposure_minutes,

    avg_temperature_c,
    avg_humidity_pct,
    max_temperature_c,
    max_humidity_pct,
    max_vibration_g,

    ROUND(temperature_severity, 2) AS temperature_severity,
    ROUND(humidity_severity, 2) AS humidity_severity,

    ROUND(estimated_spoilage_pct, 2) AS estimated_spoilage_pct,

    ROUND(
        quantity_kg * estimated_spoilage_pct / 100.0,
        2
    ) AS estimated_spoiled_quantity_kg,

    ROUND(
        quantity_kg
        - (quantity_kg * estimated_spoilage_pct / 100.0),
        2
    ) AS estimated_usable_quantity_kg

FROM spoilage_calculation