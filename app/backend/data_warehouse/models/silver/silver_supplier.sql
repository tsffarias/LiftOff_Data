{{ config(materialized='view') }}

WITH silver_suppliers AS (
  SELECT
    supplier_id,
    company_name,
    contact_name,
    email,
    phone_number,
    website,
    address,
    product_categories,
    primary_product,
    created_at
  FROM {{ source('liftoff','suppliers') }}
  WHERE email IS NOT NULL
    AND created_at <= CURRENT_DATE
)

SELECT * FROM silver_suppliers;
