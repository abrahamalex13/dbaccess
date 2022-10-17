from dotenv import load_dotenv
import os
import pytest

import dbaccess as dbac

load_dotenv()


@pytest.fixture(scope="session")
def aws_rds_specs():

    return {
        'drivername': 'postgresql'
        , 'username': os.environ.get('USER_DB')
        , 'password': 'AWS_RDS_IAM_TOKEN'
        , 'host': os.environ.get('ENDPOINT_DB')
        , 'port': os.environ.get('PORT_DB')
        , 'database': os.environ.get('NAME_DB')
        , 'region': os.environ.get('REGION_DB')
        , 'query': {'sslmode': 'require'}
        }


@pytest.fixture(scope="session")
def aws_rds_engine(aws_rds_specs):
    return dbac.create_engine_from_specs(aws_rds_specs)


@pytest.fixture(scope="session")
def aws_rds_access_authenticator(aws_rds_specs):
    return dbac.DBAccessAuthenticator(aws_rds_specs).authenticate()
