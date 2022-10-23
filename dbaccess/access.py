import sqlalchemy
from dbaccess import get_authenticator

KEYWORDS_GENERATE_AUTH_TOKEN = ["AWS_RDS_IAM_TOKEN"]
KEYS_DB_ARGS_URL = [
    'drivername', 'username', 'password', 'host'
    , 'port', 'database', 'query'
]

def create_engine_from_details(db_details, service_client_details=None):
    """
    Create a `sqlalchemy` connection engine from database implementation details. 
    Do so by: automating construction of engine URL, 
    generating connection auth token (if prompted by db password).

    Parameters
    ----------
    db_details : dict
        Dict of database implementation details keywords & values.
        Used to construct `sqlalchemy` connection engine URL
        (authenticating connection if prompted).
        Example keywords include: drivername, username, password, host, port, 
        database [name], region, query. 
        
        Prompt auth token generation via `password` key: AWS_RDS_IAM_TOKEN.

    service_client_details : dict
        Dict of [cloud computing] service client keywords & values.
        Used to instantiate service client session,
        through commands from a package like `boto3`. 
        Example keywords include: profile_name, region_name.

    """

    need_auth_token = db_details["password"] in KEYWORDS_GENERATE_AUTH_TOKEN

    if need_auth_token:
        authenticator = get_authenticator(db_details)(db_details, service_client_details)
        authenticator.authenticate()
        db_details['password'] = authenticator.token

    db_details_url = {}
    for key in KEYS_DB_ARGS_URL:
        db_details_url[key] = db_details[key]
    url_engine = sqlalchemy.engine.URL.create(**db_details_url)

    engine = sqlalchemy.create_engine(url_engine)

    return engine