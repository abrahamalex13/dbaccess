import boto3
import sqlalchemy

KEYWORDS_GENERATE_AUTH_TOKEN = [
    "AWS_IAM_TOKEN"
]

def create_engine_from_specs(db_specs):

    need_auth_token = db_specs["password"] in KEYWORDS_GENERATE_AUTH_TOKEN

    if need_auth_token:

        session = boto3.Session()
        client = session.client(service_name='rds', region_name=db_specs['region'])
        db_specs['password'] = client.generate_db_auth_token(
            DBHostname=db_specs['host']
            , Port=db_specs['port']
            , DBUsername=db_specs['username']
            , Region=db_specs['region']
        )
        del db_specs['region']

    url_engine = sqlalchemy.engine.URL.create(**db_specs)

    engine = sqlalchemy.create_engine(url_engine)

    return engine