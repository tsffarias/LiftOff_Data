{{ config(materialized='view') }}

WITH sales_seven_days_seller AS (
    SELECT 
        email AS vendedor, 
        DATE(data) AS data, 
        SUM(valor) AS total_valor, 
        SUM(quantidade) AS total_quantidade, 
        COUNT(*) AS total_vendas
    FROM 
        {{ ref('silver_sales') }}
    WHERE 
        data >= CURRENT_DATE - INTERVAL '6 days'
    GROUP BY 
        email, DATE(data)
)

SELECT 
    vendedor, 
    data, 
    total_valor, 
    total_quantidade, 
    total_vendas
FROM 
    sales_seven_days_seller
ORDER BY 
    data ASC, vendedor ASC