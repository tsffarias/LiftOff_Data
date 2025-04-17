{{ config(schema='gold', materialized='table') }}

WITH product_counts AS (
  SELECT
    email_fornecedor    AS supplier_email,
    COUNT(*)            AS total_produtos_fornecidos
  FROM {{ ref('silver_products') }}
  GROUP BY email_fornecedor
)

SELECT
  s.supplier_id,
  s.company_name,
  pc.total_produtos_fornecidos
FROM product_counts pc
JOIN {{ ref('silver_suppliers') }} s
  ON s.email = pc.supplier_email
ORDER BY pc.total_produtos_fornecidos DESC;
