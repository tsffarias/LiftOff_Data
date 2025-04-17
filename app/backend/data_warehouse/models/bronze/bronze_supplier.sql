with sources as (
    select
        supplier_id,
        company_name,
        contact_name,
        email,
        phone_number,
        website,
        address,
        product_categories,
        primary_product,
        created_at
    from {{ source('liftoff', 'suppliers') }}
)

select * from sources
