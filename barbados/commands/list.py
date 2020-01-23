import argparse
import sys
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory
from barbados.connectors import PostgresqlConnector


class List:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        conn = PostgresqlConnector()
        sess = conn.Session()

        table_scan_results = sess.query(CocktailModel).all()

        for result in table_scan_results:
            c = CocktailFactory.model_to_obj(result)
            print(c.serialize())

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='List cocktails in the database',
                                         usage='drink list')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
