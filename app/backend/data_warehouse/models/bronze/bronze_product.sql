with sources as (
    select
        id,
        name,
        description,
        price,
        categoria,
        email_fornecedor,
        created_at
    from {{ source('liftoff', 'products') }}
)

select * from sources