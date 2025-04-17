{{ config(schema='gold', materialized='table') }}

WITH sales_by_product AS (
  SELECT
    name_product      AS produto,
    SUM(price)        AS total_receita_30d,
    SUM(quantity)     AS total_qtd_30d,
    AVG(price)        AS avg_valor_30d
  FROM {{ ref('silver_sales') }}
  WHERE 
    price > 0
    AND date <= CURRENT_DATE
    AND date >= CURRENT_DATE - INTERVAL '29 days'
  GROUP BY name_product
)

SELECT
  sp.produto,
  sp.total_receita_30d,
  sp.total_qtd_30d,
  ROUND(sp.avg_valor_30d,2) AS avg_valor_30d
FROM sales_by_product sp
ORDER BY total_receita_30d DESC;
