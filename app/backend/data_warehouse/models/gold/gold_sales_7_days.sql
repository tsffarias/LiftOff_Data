{{ config(materialized='view') }}

WITH sales_seven_days AS (
    SELECT 
        data, 
        produto, 
        SUM(valor) AS total_valor, 
        SUM(quantidade) AS total_quantidade, 
        COUNT(*) AS total_vendas
    FROM 
        {{ ref('silver_sales') }}
    WHERE 
        data >= CURRENT_DATE - INTERVAL '6 days'
    GROUP BY 
        data, produto
)

SELECT 
    data, 
    produto, 
    total_valor, 
    total_quantidade, 
    total_vendas
FROM 
    sales_seven_days
ORDER BY 
    data ASC