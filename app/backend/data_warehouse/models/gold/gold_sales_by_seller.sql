{{ config(schema='gold', materialized='table') }}

WITH sales_seven_days_seller AS (
    SELECT 
        email_employee, 
        DATE(date) AS date, 
        SUM(sales_value) AS total_sales_value, 
        SUM(quantity) AS total_quantity, 
        COUNT(*) AS total_sales
    FROM 
        {{ ref('silver_sales') }}
    WHERE 
        date >= CURRENT_DATE - INTERVAL '6 days'
    GROUP BY 
        email_employee, DATE(date)
)

SELECT 
    email_employee, 
    date, 
    total_sales_value, 
    total_quantity, 
    total_sales
FROM 
    sales_seven_days_seller
ORDER BY 
    date ASC, email_employee ASC

