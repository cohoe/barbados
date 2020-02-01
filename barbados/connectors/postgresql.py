import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from barbados.models import CocktailModel, IngredientModel


class PostgresqlConnector:

    def __init__(self, username, password, database, host='127.0.0.1', port=5432):
        self.connection_string = "postgres://%s:%s@%s:%i/%s" % (username, password, host, port, database)

        engine = sqlalchemy.create_engine(self.connection_string)
        self.Session = sessionmaker(bind=engine)
        self.connection = engine.connect()

    def fetch_all_cocktails(self):
        session = self.Session(bind=self.connection)
        cocktails = session.query(CocktailModel).all()
        for cocktail in cocktails:
            print(cocktail)

    def save(self, model_object):
        session = self.Session(bind=self.connection)
        session.add(model_object)
        session.commit()
