import DBAccess as dbac

def test_prune_db_specs_blueprint_kwargs(aws_rds_specs0):

    kwargs = aws_rds_specs0 \
        .extract_blueprint_kwargs(dbac.AWSRDSSpecs)

    assert 'self' not in kwargs

def test_drop_singletons_aws_rds_db_specs_format(aws_rds_specs):
    """
    Format method should yield dictionaries which
    organize all original singleton arguments.
    """

    db_specs_keys = list(aws_rds_specs.__dict__.keys())
    keys_expected = [
        'api_service', 'connectivity', 
        'login_credentials', 'cloud_platform',
        'engine_name'
        ]
    assert db_specs_keys == keys_expected
