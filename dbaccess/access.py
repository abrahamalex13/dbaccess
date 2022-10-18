import sqlalchemy
from dbaccess import get_authenticator

KEYWORDS_GENERATE_AUTH_TOKEN = ["AWS_RDS_IAM_TOKEN"]
KEYS_DB_SPECS_URL = [
    'drivername', 'username', 'password', 'host'
    , 'port', 'database', 'query'
]

def create_engine_from_specs(db_specs, service_client_specs=None):
    """
    Create a `sqlalchemy` connection engine from database specification details. 
    Do so by: automating construction of engine URL, 
    generating connection auth token (if prompted by db_specs password).

    Parameters
    ----------
    db_specs : dict
        Dict of database specification keywords & values.
        Used to construct `sqlalchemy` connection engine URL
        (authenticating connection if prompted).
        Example keywords include: drivername, username, password, host, port, 
        database [name], region, query. 
        
        Prompt auth token generation via `password` key: AWS_RDS_IAM_TOKEN.

    service_client_specs : dict
        Dict of [cloud computing] service client keywords & values.
        Used to instantiate service client session,
        through commands from a package like `boto3`. 
        Example keywords include: profile_name, region_name.

    """

    need_auth_token = db_specs["password"] in KEYWORDS_GENERATE_AUTH_TOKEN

    if need_auth_token:
        authenticator = get_authenticator(db_specs)(db_specs, service_client_specs)
        authenticator.authenticate()
        db_specs['password'] = authenticator.token

    db_specs_url = {}
    for key in KEYS_DB_SPECS_URL:
        db_specs_url[key] = db_specs[key]
    url_engine = sqlalchemy.engine.URL.create(**db_specs_url)

    engine = sqlalchemy.create_engine(url_engine)

    return engine