import sqlalchemy
import barbados.config
from sqlalchemy.orm import sessionmaker, Session
from barbados.models import CocktailModel


class PostgresqlConnector:
    db_string = "postgres://%s:%s@%s:%i/%s" % (barbados.config.database.postgres_username,
                                               barbados.config.database.postgres_password,
                                               barbados.config.database.postgres_host,
                                               barbados.config.database.postgres_port,
                                               barbados.config.database.postgres_database)

    engine = sqlalchemy.create_engine(db_string)
    Session = sessionmaker(bind=engine)

    def __init__(self):
        self.connection = self.engine.connect()

    def fetch_all_cocktails(self):
        session = Session(bind=self.connection)
        cocktails = session.query(CocktailModel).all()
        for cocktail in cocktails:
            print(cocktail)

    def save(self, model_object):
        session = Session(bind=self.connection)
        session.add(model_object)
        session.commit()
