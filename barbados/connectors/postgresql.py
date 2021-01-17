import sqlalchemy
from sqlalchemy.orm import sessionmaker
from barbados.models.base import BarbadosModel
from barbados.services.logging import LogService
from barbados.settings import Setting
from contextlib import contextmanager


class PostgresqlConnector:
    """
    Connector to PostgreSQL.
    Unfortunately I didn't write down all of the various StackOverflow
    and tutorial posts that certainly got this code to work.
    """

    def __init__(self):
        """
        @TODO password change!
        """
        self.username = Setting(path='/database/postgres/username', env='AMARI_DATABASE_USERNAME', default='amari', type_=str).get_value()
        self.password = Setting(path='/database/postgres/password', env='AMARI_DATABASE_PASSWORD', default='s3krAt', type_=str).get_value()
        self.host = Setting(path='/database/postgres/host', env='AMARI_DATABASE_HOST', default='127.0.0.1', type_=str).get_value()
        self.port = Setting(path='/database/postgres/port', env='AMARI_DATABASE_PORT', default=5432, type_=int).get_value()
        self.database = Setting(path='/database/postgres/database', env='AMARI_DATABASE_NAME', default='amari', type_=str).get_value()
        self.debug_sql = Setting(path='/database/postgres/debug_sql', env='AMARI_DATABASE_DEBUG_SQL', default=False, type_=bool).get_value()

        connection_string = "postgres://%s:%s@%s:%i/%s" % (self.username, self.password, self.host, self.port, self.database)
        LogService.info("Postgres string: %s" % connection_string)
        LogService.warn("Starting PostgreSQL connection!")

        self.engine = sqlalchemy.create_engine(connection_string, echo=self.debug_sql)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self):
        BarbadosModel.metadata.create_all(self.engine)

    def drop_all(self):
        BarbadosModel.metadata.drop_all(self.engine)

    @contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
