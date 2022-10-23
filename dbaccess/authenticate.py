# Official AWS docs: 
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
import boto3


def get_authenticator(db_details):
    """
    Return Authenticator class based on database implementation details.
    """

    if 'AWS_RDS' in db_details['password'].upper():
        return AWSRDSAccessAuthenticator
    else:
        raise Exception("No corresponding authenticator object.")


class AWSRDSAccessAuthenticator:
    """
    Generate auth token for database connection,
    and store prerequisite cloud service client details.

    Parameters
    ----------
    db_details : dict
        Dict of database implementation details keywords & values.
        Example keywords include: drivername, username, password, host, port, 
        database [name], region, query. 
        
        Prompt auth token generation via `password` key: AWS_RDS_IAM_TOKEN.

    service_client_details : dict
        Dict of [cloud computing] service client keywords & values.
        Used to instantiate service client session,
        through commands from a package like `boto3`. 
        Example keywords include: profile_name, region_name.

    """

    def __init__(self, db_details, service_client_details=None):

        self.db_details = db_details

        if service_client_details is not None:
            self.service_client_details = service_client_details
        else:
            self.service_client_details = {
                'profile_name': None, 'region_name': self.db_details['region']
                }

    def authenticate(self):

        self.initialize_service_client()
        self.generate_auth_token()

    def initialize_service_client(self):

        self.session = boto3.Session(
            profile_name=self.service_client_details['profile_name']
            )
        
        self.client = self.session.client('rds'
            , region_name=self.service_client_details['region_name'] 
            )

    def generate_auth_token(self):

        kwargs = {
            'DBHostname': self.db_details['host']
            , 'Port': self.db_details['port']
            , 'DBUsername': self.db_details['username']
            , 'Region': self.db_details['region']
            }

        self.token = self.client.generate_db_auth_token(**kwargs)
