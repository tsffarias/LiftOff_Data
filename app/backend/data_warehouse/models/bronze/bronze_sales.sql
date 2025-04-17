with sources as (
    select
        id,
        email_employee,
        email_customer,
        first_name,
        last_name,
        phone_number,
        price,
        quantity,
        name_product,
        date,
        created_at
    from {{ source('liftoff', 'sales') }}
)

select * from sources