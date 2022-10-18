# Official AWS docs: 
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
import boto3


def get_authenticator(db_specs):
    """
    Return Authenticator class based on database specification details.
    """

    if 'AWS' in db_specs['password'].upper():
        return AWSRDSAccessAuthenticator
    else:
        raise Exception("No corresponding authenticator object.")


class AWSRDSAccessAuthenticator:
    """
    Generate auth token for database connection,
    and store prerequisite cloud service client details.

    Parameters
    ----------
    db_specs : dict
        Dict of database specification keywords & values.
        Example keywords include: drivername, username, password, host, port, 
        database [name], region, query. 
        
        Prompt auth token generation via `password` key: AWS_RDS_IAM_TOKEN.

    service_client_specs : dict
        Dict of [cloud computing] service client keywords & values.
        Used to instantiate service client session,
        through commands from a package like `boto3`. 
        Example keywords include: profile_name, region_name.

    """

    def __init__(self, db_specs, service_client_specs=None):

        self.db_specs = db_specs

        if service_client_specs is not None:
            self.service_client_specs = service_client_specs
        else:
            self.service_client_specs = {
                'profile_name': None, 'region_name': self.db_specs['region']
                }

    def authenticate(self):

        self.initialize_service_client()
        self.generate_auth_token()

    def initialize_service_client(self):

        self.session = boto3.Session(
            profile_name=self.service_client_specs['profile_name']
            )
        
        self.client = self.session.client('rds'
            , region_name=self.service_client_specs['region_name'] 
            )

    def generate_auth_token(self):

        kwargs = {
            'DBHostname': self.db_specs['host']
            , 'Port': self.db_specs['port']
            , 'DBUsername': self.db_specs['username']
            , 'Region': self.db_specs['region']
            }

        self.token = self.client.generate_db_auth_token(**kwargs)
