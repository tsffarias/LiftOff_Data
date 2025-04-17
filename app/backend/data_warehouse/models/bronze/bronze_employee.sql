with sources as (
    select
        employee_id,
        first_name,
        last_name,
        email,
        phone_number,
        hire_date,
        job_title,
        location,
        birth_date,
        gender,
        nationality,
        start_date,
        salary,
        termination_date,
        created_at,
        manager_id,
        department_id
    from {{ source('liftoff', 'employees') }}
)

select * from sources