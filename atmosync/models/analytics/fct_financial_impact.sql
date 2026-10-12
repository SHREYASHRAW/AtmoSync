{{ config(
    materialized='view'
) }}

WITH spoilage AS (

    SELECT *
    FROM {{ ref('fct_spoilage') }}

),

market_prices AS (

    SELECT
        commodity,
        market,
        price_per_kg
    FROM {{ ref('commodity_market_prices') }}

),

financial_impact AS (

    SELECT
        s.container_id,
        s.commodity,
        s.quantity_kg,
        s.origin,
        s.destination,

        s.estimated_spoilage_pct,
        s.estimated_spoiled_quantity_kg,
        s.estimated_usable_quantity_kg,

        p.price_per_kg AS destination_price_per_kg,

        ROUND(
            s.quantity_kg * p.price_per_kg,
            2
        ) AS estimated_total_market_value,

        ROUND(
            s.estimated_spoiled_quantity_kg * p.price_per_kg,
            2
        ) AS estimated_spoilage_loss,

        ROUND(
            s.estimated_usable_quantity_kg * p.price_per_kg,
            2
        ) AS estimated_usable_value

    FROM spoilage AS s

    LEFT JOIN market_prices AS p
        ON LOWER(s.commodity) = LOWER(p.commodity)
        AND LOWER(s.destination) = LOWER(p.market)

)

SELECT *
FROM financial_impact