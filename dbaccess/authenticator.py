# Interface for authenticating database access.
import boto3
import inspect

class AWSRDSAccessAuthenticator:

    def __init__(self, db_specs):
        self.db_specs = db_specs

    def initialize_db_service(self):

        self.session = boto3.Session(
            profile_name=self.db_specs.api_service['profile_name']
            )
        
        self.client = self.session.client('rds'
            , region_name=self.db_specs.connectivity['region'] 
            )

    def format_args_generate_auth_token(self):
        """
        Construct dict of properly-named arguments for
        generate_db_auth_token function. 
        Given general lowcase specs, automate special capitalization, etc.
        """

        self.args_generate_auth_token = {
            'DBHostname': self.db_specs.connectivity['host']
            , 'Port': self.db_specs.connectivity['port']
            , 'DBUsername': self.db_specs.login_credentials['user']
            , 'Region': self.db_specs.connectivity['region']
            }

    def generate_auth_token(self):

        self.format_args_generate_auth_token()
        self.token = self.client.generate_db_auth_token(
            **self.args_generate_auth_token
            )

    def authenticate(self):

        self.initialize_db_service()
        self.generate_auth_token()


class DBAccessAuthenticator:
    """
    Interface for authenticating access to arbitrary database.
    Implements authentication according to database specifications.

    Parameters
    ----------
    db_specs: DBSpecs, a formatted database specification object. 
    """

    def __init__(self, db_specs):
        self.db_specs = db_specs

    def get_blueprint(self):

        if self.db_specs.cloud_platform == 'aws_rds':
            blueprint = AWSRDSAccessAuthenticator
        else:
            blueprint = None

        return blueprint

    def authenticate(self):

        authenticator_blueprint = self.get_blueprint()
        authenticator = authenticator_blueprint(self.db_specs)
        authenticator.authenticate()

        return authenticator
