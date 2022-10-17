def test_aws_rds_engine(aws_rds_engine):
    
    with aws_rds_engine.connect() as conn:
        conn.exec_driver_sql("SELECT 2")