import sqlalchemy
from sqlalchemy.orm import sessionmaker
from barbados.models.base import BarbadosModel
from barbados.services.logging import Log


class PostgresqlConnector:

    def __init__(self, username, password, database, host='127.0.0.1', port=5432, debug_sql=False):
        connection_string = "postgres://%s:%s@%s:%i/%s" % (username, password, host, port, database)
        Log.info("Using Postgres host: \"%s\"" % host)

        self.engine = sqlalchemy.create_engine(connection_string, echo=debug_sql)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self):
        BarbadosModel.metadata.create_all(self.engine)

    def drop_all(self):
        BarbadosModel.metadata.drop_all(self.engine)

    # @staticmethod
    # def commit():
    #     session.commit()
    from contextlib import contextmanager

    @contextmanager
    def get_session(self):
        # return self.Session()
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()