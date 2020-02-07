import sqlalchemy
from barbados.models.base import BarbadosModel, session


class PostgresqlConnector:

    def __init__(self, username, password, database, host='127.0.0.1', port=5432):
        connection_string = "postgres://%s:%s@%s:%i/%s" % (username, password, host, port, database)

        self.engine = sqlalchemy.create_engine(connection_string)
        session.configure(bind=self.engine)

    def create_all(self):
        BarbadosModel.metadata.create_all(self.engine)

    @staticmethod
    def commit():
        session.commit()
