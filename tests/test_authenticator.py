def test_aws_rds_access_authenticate(aws_rds_access_authenticator):
    assert hasattr(aws_rds_access_authenticator, "token")

