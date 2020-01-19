import argparse
import sys
import barbados.util
from barbados.factories import CocktailFactory


class Testcmd:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        raw_recipe = barbados.util.read_yaml_file(args.recipepath)[0]
        c = CocktailFactory.raw_to_obj(raw_recipe)

        for spec in c.specs:
            for ingredient in spec.ingredients:
                print(ingredient)
            for garnish in spec.garnish:
                print(garnish)


    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Print a cocktail object',
                                         usage='drink testcmd <recipepath>')
        parser.add_argument('recipepath', help='path to recipe yaml')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
