# Interface for an arbitrary database's specifications.
# Pass to Authenticator, Access interfaces.
import inspect

class AWSRDSSpecs:
    """
    Interface for storing database's: 
        - API service specs (activation of API service)
        - Connectivity specs
        - Login credentials
    Argument names follow from names in AWS user interface.
    Interface maps inputs to names in Python's AWS functions
    (to the extent possible).

    Parameters
    ----------
    profile_name: str, username for cloud platform account.
    endpoint: str, database url
    port: integer, address on database's server
    region: str, where database server resides
    db_name: str, database identifier
    db_user: str, username _within-database_
    """

    def __init__(self,
        profile_name,
        endpoint, port, region, db_name
        , db_user
        ):

        self.api_service = {'profile_name': profile_name}

        self.connectivity = {
            'host': endpoint
            , 'port': port
            , 'region': region
            , 'dbname': db_name
            }

        self.login_credentials = {'user': db_user}

class DBSpecs:
    """
    Interface for an arbitrary database's specifications.
    Downstream, pass to Authenticator, Access interfaces.

    Transform to final form using `.format()`.

    Parameters
    ----------
    cloud_platform: str, name of cloud services provider.
        For AWS RDS, specify cloud platform 'aws_rds'.
    profile_name: str, username for cloud platform account.
    endpoint: str, database url
    port: integer, address on database's server
    region: str, where database server resides
    db_name: str, database identifier
    db_user: str, username _within-database_
    engine_name: str, software that database uses to 
        create/read/update/delete data. 
        For PostgreSQL, specify 'postgresql'.
    """

    def __init__(self,
        cloud_platform
        , profile_name=None
        , endpoint=None, port=None
        , region=None, db_name=None
        , db_user=None
        , engine_name=None
        ):

        self.cloud_platform=cloud_platform
        self.profile_name=profile_name
        self.endpoint=endpoint
        self.port=port
        self.region=region
        self.db_name=db_name
        self.db_user=db_user
        self.engine_name=engine_name

    def get_blueprint(self):

        if self.cloud_platform == 'aws_rds':
            blueprint = AWSRDSSpecs
        else:
            blueprint = None

        return blueprint

    def extract_blueprint_kwargs(self, blueprint):
        """
        A database's class may not need all arguments
        passed to generic interface. Extract what's necessary.
        Also, preferred method for extracting 
        class blueprint's arguments unfavorably
        returns 'self' -- prune.
        """
        # blueprint (class's) "self" not a real kwarg
        kwargs_required = inspect \
            .getfullargspec(blueprint) \
            .args[1:]

        kwargs = {x: self.__dict__[x] for x in kwargs_required}

        return kwargs

    def format(self):
        """
        Transform generic db_specs object into a
        particular database's properly formatted db_specs.
        """

        db_specs_blueprint = self.get_blueprint()
        kwargs = self.extract_blueprint_kwargs(
            db_specs_blueprint
            )

        db_specs = db_specs_blueprint(**kwargs)
        db_specs.cloud_platform = self.cloud_platform
        db_specs.engine_name = self.engine_name

        return db_specs
