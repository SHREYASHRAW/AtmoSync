{{ config(
    materialized='view'
) }}

WITH financial_impact AS (
    SELECT *
    FROM {{ ref('fct_financial_impact') }}
),

market_prices AS (
    SELECT
        commodity,
        market,
        price_per_kg
    FROM {{ ref('commodity_market_prices') }}
),

route_costs AS (
    SELECT
        origin,
        destination AS alternative_market,
        route_cost
    FROM {{ ref('market_route_costs') }}
),

candidate_markets AS (
    SELECT
        f.container_id,
        f.commodity,
        f.quantity_kg,
        f.origin,
        f.destination AS current_destination,
        f.estimated_spoilage_pct,
        f.estimated_usable_quantity_kg,
        f.estimated_usable_value AS current_usable_value,

        p.market AS alternative_market,
        p.price_per_kg AS alternative_price_per_kg,
        r.route_cost

    FROM financial_impact AS f

    INNER JOIN market_prices AS p
        ON LOWER(f.commodity) = LOWER(p.commodity)
        AND LOWER(f.destination) <> LOWER(p.market)

    INNER JOIN route_costs AS r
        ON LOWER(f.origin) = LOWER(r.origin)
        AND LOWER(p.market) = LOWER(r.alternative_market)
),

arbitrage_calculation AS (
    SELECT
        *,
        
        ROUND(
            estimated_usable_quantity_kg * alternative_price_per_kg,
            2
        ) AS alternative_gross_value,

        ROUND(
            (estimated_usable_quantity_kg * alternative_price_per_kg)
            - route_cost,
            2
        ) AS alternative_net_value

    FROM candidate_markets
),

opportunity_calculation AS (
    SELECT
        *,
        
        ROUND(
            alternative_net_value - current_usable_value,
            2
        ) AS net_opportunity,

        ROUND(
            CASE
                WHEN current_usable_value > 0
                    THEN (
                        (alternative_net_value - current_usable_value)
                        / current_usable_value
                    ) * 100
                ELSE 0
            END,
            2
        ) AS opportunity_pct

    FROM arbitrage_calculation
)

SELECT
    container_id,
    commodity,
    quantity_kg,
    origin,
    current_destination,
    estimated_spoilage_pct,
    estimated_usable_quantity_kg,
    current_usable_value,
    alternative_market,
    alternative_price_per_kg,
    route_cost,
    alternative_gross_value,
    alternative_net_value,
    net_opportunity,
    opportunity_pct,

    CASE
        WHEN net_opportunity > 0
            THEN 'REROUTE_CANDIDATE'
        ELSE 'KEEP_CURRENT_ROUTE'
    END AS arbitrage_status

FROM opportunity_calculation