# Interface for accessing databases -- 
# applying prerequisite database access authentication.
import psycopg2
import sqlalchemy
import pandas.io.sql as sqlio

class PostgresDBAccess:

    def __init__(self, db_access_authenticator): 
        self.db_access_authenticator = db_access_authenticator

    def connect(self):

        self.conn = psycopg2.connect(
            host = self.db_access_authenticator.db_specs.connectivity['host']
            , port = self.db_access_authenticator.db_specs.connectivity['port']
            , dbname = self.db_access_authenticator.db_specs.connectivity['dbname']
            , user = self.db_access_authenticator.db_specs.login_credentials['user']
            , password = self.db_access_authenticator.token
            , sslmode = 'require'
            , sslrootcert = 'SSLCERTIFICATE'
            )

        self.cursor = self.conn.cursor()

        url_engine = sqlalchemy.engine.url.URL(
            drivername='postgresql'
            , username=self.db_access_authenticator.db_specs.login_credentials['user']
            , password=self.db_access_authenticator.token
            , host=self.db_access_authenticator.db_specs.connectivity['host']
            , port=self.db_access_authenticator.db_specs.connectivity['port']
            , database=self.db_access_authenticator.db_specs.connectivity['dbname']
            , query={'sslmode': 'require'}
            )

        self.engine = sqlalchemy.create_engine(url_engine)

    def read_query(self, query):
        return sqlio.read_sql_query(query, self.conn)

    def write_query(self, name_table, df, if_exists='append'):

        df.to_sql(
            name_table, self.engine, 
            if_exists=if_exists, index=False
            )

    def query(self, query):

        self.cursor.execute(query)
        self.conn.commit()

    def test_connect(self):

        try:
            result = self.query("""SELECT now()""")
            print("Test query successful.")
            response_code = 200

        except Exception as e:
            print("Database connection test failed due to {}".format(e))
            response_code = 400

        return response_code

class DBAccess:
    """
    Interface for database access -- establishing connection, querying.
    After successful `.connect()`, methods include:
        - test_connect (send basic test query to confirm connection)
        - read_query (send a query which reads data and returns)
        - write_query (send a query which writes data)
        - query (general-purpose query for other database actions)

    Parameters
    ----------
    db_access_authenticator: DBAccessAuthenticator, an Authenticator
        object which has executed `.authenticate()`.
    """

    def __init__(self, db_access_authenticator): 
        self.db_access_authenticator = db_access_authenticator

    def get_blueprint(self):

        engine_name = self \
            .db_access_authenticator.db_specs.engine_name

        if engine_name == 'postgresql':
            blueprint = PostgresDBAccess
        else:
            blueprint = None

        return blueprint

    def connect(self):

        blueprint = self.get_blueprint()
        db_access = blueprint(self.db_access_authenticator)
        db_access.connect()

        return db_access
