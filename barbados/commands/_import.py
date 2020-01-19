import argparse
import sys
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory


class Import:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        c = CocktailFactory.obj_from_file(args.recipepath)
        print("Working %s" % args.recipepath)

        print(c.serialize())

        ddb = CocktailModel(**c.serialize())
        ddb.save()



    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Index a cocktail object',
                                         usage='drink index <recipepath>')
        parser.add_argument('recipepath', help='name of yaml file to create')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass