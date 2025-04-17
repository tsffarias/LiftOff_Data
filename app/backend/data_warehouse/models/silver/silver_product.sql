{{ config(materialized='view') }}

WITH silver_products AS (
  SELECT
    id,
    name,
    description,
    ROUND(CAST(price AS DECIMAL(12,2)),2) AS price,
    categoria,
    email_fornecedor,
    created_at
  FROM {{ source('liftoff','products') }}
  WHERE price > 0
    AND created_at <= CURRENT_DATE
)

SELECT * FROM silver_products;
