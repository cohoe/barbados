import argparse
import sys
import barbados.util
from barbados.factories import CocktailFactory


class Search:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        recipe_files = barbados.util.list_files('./data/recipes/')

        drinks = {}

        for file in recipe_files:
            file_path = "./data/recipes/%s" % file
            raw_recipe = barbados.util.read_yaml_file(file_path)[0]
            c = CocktailFactory.raw_to_obj(raw_recipe)

            for spec in c.specs:
                for ingredient in spec.ingredients:
                    if args.ingredient.upper() in ingredient.name.upper():
                        drink_ingredients = []
                        for ing in spec.ingredients:
                            drink_ingredients.append(ing.name)
                        drinks[c.name] = drink_ingredients

        for drink in drinks.keys():
            print(drink + " (" + ', '.join(drinks[drink]) + ')')

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Search for an ingredient',
                                         usage='drink search <ingredient>')
        parser.add_argument('ingredient', help='string to search for')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
