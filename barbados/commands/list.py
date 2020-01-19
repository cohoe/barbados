import argparse
import sys
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory


class List:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)





    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='List cocktails in the database',
                                         usage='drink list')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
