import sqlalchemy
from dbaccess import get_authenticator

KEYWORDS_GENERATE_AUTH_TOKEN = ["AWS_RDS_IAM_TOKEN"]
KEYS_DB_SPECS_URL = [
    'drivername', 'username', 'password', 'host'
    , 'port', 'database', 'query'
]

def create_engine_from_specs(db_specs, service_client_specs=None):

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