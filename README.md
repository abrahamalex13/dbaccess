# `dbaccess`: One Python Interface for Accessing Any Database

It is challenging to keep track of the many Python interfaces
used for database connection. Moreover, for many cases,
a single interface should do. The fundamental steps for 
database connection don't vary too much:

- Organize/declare database specifications, such as:
    - Cloud platform name
    - Cloud platform account profile/user name
    - Endpoint URL and port
    - Database's name
    - Database account's user name
    - Database engine name

- Authenticate database access, which may involve:
    - Generating an access token
        - AWS IAM

- Establish database connection
    - Use prerequisite authentication result
    and database specs.

Translate the above steps to a fundamental code workflow:
```
    import dbaccess as dbac
    
    db_specs = dbac.DBSpecs(...).format()
    db_access_authenticator = dbac.DBAccessAuthenticator(db_specs).authenticate()
    db_access = dbac.DBAccess(db_access_authenticator).connect()

    # give connection a final test, and proceed!
    db_access.test_query(...)
    db_access.query(...)
```