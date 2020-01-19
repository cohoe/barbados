import argparse
import sys
import os
import barbados.util
from barbados.factories import CocktailFactory
from barbados.printers import KitchenCardPrinter, MenuPrinter


class Render:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        if args.recipepath:
            self._render_recipe(args=args)
        elif args.menupath:
            self._render_menu(args=args)

    @staticmethod
    def _render_menu(args):
        raw_menu = barbados.util.read_yaml_file(args.menupath)

        sections = []
        for section in raw_menu:
            print("Section %s" % section['name'])
            cocktails = []
            for recipe in section['recipes']:
                print("Recipe %s" % recipe)
                recipe_file_path = os.path.join(args.datadir, recipe + '.yaml')
                c = CocktailFactory.obj_from_file(recipe_file_path)
                cocktails.append(c)
            sections.append({
                'name': section['name'],
                'cocktails': cocktails
            })

        mp = MenuPrinter()
        mp.render(sections=sections)

    @staticmethod
    def _render_recipe(args):
        c = CocktailFactory.obj_from_file(args.recipepath)

        kcp = KitchenCardPrinter()
        kcp.render(cocktail=c, specindex=0)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Print a cocktail object',
                                         usage='drink testcmd <recipepath>')
        parser.add_argument('-r', '--recipe', help='path to recipe yaml',
                            required=False, dest='recipepath')
        parser.add_argument('-m', '--menu', help='path to menu yaml',
                            required=False, dest='menupath')
        parser.add_argument('-d', '--data', help='data directory for menu recipes',
                            default='./data/recipes', required=False, dest='datadir')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        if args.recipepath is None and args.menupath is None:
            barbados.util.die('Must specify one of either --recipe or --menu')
        if args.recipepath and args.menupath:
            barbados.util.die('Only specify one of either --recipe or --menu')
