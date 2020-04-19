import sqlalchemy
from barbados.models.base import BarbadosModel, session
from barbados.services import logging


class SqliteConnector:

    def __init__(self, path):
        connection_string = "sqlite:///%s" % path
        logging.info("connection string is '%s'" % connection_string)

        self.engine = sqlalchemy.create_engine(connection_string)
        session.configure(bind=self.engine)

    @staticmethod
    def commit():
        session.commit()
