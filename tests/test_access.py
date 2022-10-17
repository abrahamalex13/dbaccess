def test_pg_engine(pg_engine):
    
    with pg_engine.connect() as conn:
        conn.exec_driver_sql("SELECT 2")