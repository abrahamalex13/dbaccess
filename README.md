# `dbaccess`: Helper for Database Authentication and Connection

`dbaccess` aims to decrease analysts' time-to-data analysis,
by abstracting away the boilerplate of database authentication and connection. 
There are low-level details standard in calls to `boto3`, `sqlalchemy`, etc; 
`dbaccess` handles those standard details for you. 
**`boto3`, `sqlalchemy`, etc are already well-formulated -- 
so `dbaccess` simply encapsulates typical workflows.**

Ultimately, `dbaccess` returns a `sqlalchemy` engine,
with less boilerplate to get there.

## Getting Started

```
    from dotenv import load_dotenv
    import os
    import dbaccess as dbac

    load_dotenv()
    
    engine = dbac.create_engine_from_specs({
        'drivername': 'postgresql'
        , 'username': os.environ.get('USER_DB')
        , 'password': 'AWS_RDS_IAM_TOKEN'
        , 'host': os.environ.get('ENDPOINT_DB')
        , 'port': os.environ.get('PORT_DB')
        , 'database': os.environ.get('NAME_DB')
        , 'region': os.environ.get('REGION_DB')
        , 'query': {'sslmode': 'require'}
        })

    # give connection a test!
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 2")
```