def test_aws_rds_authenticate(aws_rds_authenticator):
    aws_rds_authenticator.authenticate()
    assert hasattr(aws_rds_authenticator, "token")

