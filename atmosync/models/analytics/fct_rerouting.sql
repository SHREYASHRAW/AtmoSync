{{ config(
    materialized='view'
) }}

WITH ranked_opportunities AS (
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
        arbitrage_status,

        ROW_NUMBER() OVER (
            PARTITION BY container_id
            ORDER BY net_opportunity DESC
        ) AS opportunity_rank

    FROM {{ ref('fct_arbitrage') }}
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
    alternative_market AS recommended_destination,
    alternative_price_per_kg,
    route_cost,
    alternative_gross_value,
    alternative_net_value,
    net_opportunity,
    opportunity_pct,

    CASE
        WHEN net_opportunity > 0
            THEN 'REROUTE'
        ELSE 'KEEP_CURRENT_ROUTE'
    END AS routing_decision,

    CASE
        WHEN net_opportunity > 0
            THEN 'Positive simulated net value opportunity'
        ELSE 'No positive simulated net value opportunity'
    END AS decision_reason

FROM ranked_opportunities
WHERE opportunity_rank = 1