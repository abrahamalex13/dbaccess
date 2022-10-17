from dotenv import load_dotenv
import os
import pytest

import dbaccess as dbac

load_dotenv()


@pytest.fixture(scope="session")
def pg_engine():

    engine = dbac.create_engine_from_specs({
        'drivername': 'postgresql'
        , 'username': os.environ.get('USER_DB')
        , 'password': 'AWS_IAM_TOKEN'
        , 'host': os.environ.get('ENDPOINT_DB')
        , 'port': os.environ.get('PORT_DB')
        , 'database': os.environ.get('NAME_DB')
        , 'region': os.environ.get('REGION_DB')
        , 'query': {'sslmode': 'require'}
        })

    return engine


@pytest.fixture(scope="session")
def aws_rds_specs0():

    db_specs = dbac.DBSpecs(
        cloud_platform="aws_rds",
        profile_name="default",
        endpoint=os.environ.get("ENDPOINT_DB"),
        port=os.environ.get("PORT_DB"),
        region=os.environ.get("REGION_DB"),
        db_name=os.environ.get("NAME_DB"),
        db_user=os.environ.get("USER_DB"),
        engine_name="postgresql",
    )

    return db_specs


@pytest.fixture(scope="session")
def aws_rds_specs(aws_rds_specs0):
    return aws_rds_specs0.format()


@pytest.fixture(scope="session")
def aws_rds_access_authenticator(aws_rds_specs):
    return dbac.DBAccessAuthenticator(aws_rds_specs).authenticate()
