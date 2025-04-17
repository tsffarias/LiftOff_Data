{{ config(schema='gold', materialized='table') }}

WITH sales_seven_days AS (
    SELECT 
        date, 
        name_product, 
        SUM(sales_value) AS total_sales_value, 
        SUM(quantity) AS total_quantity, 
        COUNT(*) AS total_sales
    FROM 
        {{ ref('silver_sales') }}
    WHERE 
        date >= CURRENT_DATE - INTERVAL '6 days'
    GROUP BY 
        date, name_product
)

SELECT 
    date, 
    name_product, 
    total_sales_value, 
    total_quantity, 
    total_sales
FROM 
    sales_seven_days
ORDER BY 
    date ASC



