{{ config(materialized='view') }}

WITH silver_employees AS (
  SELECT
    employee_id,
    manager_id,
    first_name,
    last_name,
    email,
    phone_number,
    hire_date,
    department_id,
    job_title,
    location,
    birth_date,
    gender,
    nationality,
    start_date,
    ROUND(CAST(salary AS DECIMAL(12,2)),2) AS salary,
    termination_date,
    created_at
  FROM {{ source('liftoff','employees') }}
  WHERE email IS NOT NULL
    AND hire_date <= CURRENT_DATE
)

SELECT * FROM silver_employees;
