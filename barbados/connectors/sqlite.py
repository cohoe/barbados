import sqlalchemy
from sqlalchemy.orm import sessionmaker
# from barbados.models.base import BarbadosModel, session
from barbados.services.logging import Log


class SqliteConnector:

    def __init__(self, path):
        connection_string = "sqlite:///%s" % path
        Log.info("connection string is '%s'" % connection_string)

        self.engine = sqlalchemy.create_engine(connection_string)
        # session.configure(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
