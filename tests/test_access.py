def test_pg_connect(pg_db_access):
    response = pg_db_access.test_connect()
    assert response == 200
