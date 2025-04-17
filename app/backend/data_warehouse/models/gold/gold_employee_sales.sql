-- gold_employee_sales.sql
{{ config(schema='gold', materialized='table') }}

WITH sales_by_employee AS (
  SELECT
    email_employee     AS employee_email,
    SUM(price)         AS total_receita_7d,
    SUM(quantity)      AS total_qtd_7d,
    COUNT(*)           AS total_transacoes_7d
  FROM {{ ref('silver_sales') }}
  WHERE 
    price > 0
    AND date <= CURRENT_DATE
    AND date >= CURRENT_DATE - INTERVAL '6 days'
  GROUP BY email_employee
)

SELECT
  e.employee_id,
  e.first_name || ' ' || e.last_name AS employee_name,
  se.total_receita_7d,
  se.total_qtd_7d,
  se.total_transacoes_7d
FROM sales_by_employee se
JOIN {{ ref('silver_employees') }} e
  ON e.email = se.employee_email
ORDER BY se.total_receita_7d DESC;
