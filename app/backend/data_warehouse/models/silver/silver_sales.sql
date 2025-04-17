{{ config(materialized='view') }}

WITH silver_sales AS (
    SELECT 
        DATE(date) AS date,
        id,
        email_employee,
        email_customer,
        first_name,
        last_name,
        phone_number,
        name_product,
        quantity,
        round(cast(price as decimal(10, 2)), 2) as sales_value,
        created_at
    FROM 
        {{ ref('bronze_sales') }}
    WHERE 
        price > 0 
        AND price < 8000
        AND date <= CURRENT_DATE
)

SELECT * FROM silver_sales

        