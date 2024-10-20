{{ config(materialized='view') }}

select * from {{ source('raw_sales', 'sales') }}