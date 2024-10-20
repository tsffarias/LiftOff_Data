{{ config(materialized='view') }}

WITH silver_sales AS (
    SELECT 
        email, 
        DATE(data) AS data,
        valor, 
        quantidade, 
        produto
    FROM 
        {{ ref('bronze_sales') }}
    WHERE 
        valor > 0 
        AND valor < 8000
        AND data <= CURRENT_DATE
)

SELECT * FROM silver_sales