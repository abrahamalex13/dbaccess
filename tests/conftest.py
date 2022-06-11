from dotenv import load_dotenv
import os
import pytest

import DBAccess as dbac

load_dotenv()

@pytest.fixture(scope="session")
def aws_rds_specs0():

    db_specs = dbac.DBSpecs(
        cloud_platform='aws_rds'
        , profile_name='default'
        , endpoint=os.environ.get('ENDPOINT_DB')
        , port=os.environ.get('PORT_DB')
        , region=os.environ.get('REGION_DB')
        , db_name=os.environ.get('NAME_DB')
        , db_user=os.environ.get('USER_DB')
        , engine_name='postgresql'
        )

    return db_specs

@pytest.fixture(scope="session")
def aws_rds_specs(aws_rds_specs0):
    return aws_rds_specs0.format()

@pytest.fixture(scope="session")
def aws_rds_access_authenticator(aws_rds_specs):
    return dbac.DBAccessAuthenticator(aws_rds_specs).authenticate()

@pytest.fixture(scope="session")
def pg_db_access(aws_rds_access_authenticator):

    db_access = dbac.DBAccess(
        aws_rds_access_authenticator
        ).connect()

    return db_access
