import os
import sys
import pdfkit
import argparse
import barbados.util


class Print:
    def __init__(self):
        pass

    def run(self):
        # @TODO this is all prototype code
        # @TODO this should not be called print()
        args = self._setup_args()
        self._validate_args(args)

        raw_ingredients = barbados.util.read_yaml_file('./data/ingredients.yaml')
        ingredients = {}
        for ingredient in raw_ingredients:
            ingredients[ingredient['name']] = ingredient

        jt = barbados.util.load_template_from_file('./templates/print.j2')

        drink = barbados.util.read_yaml_file(args.recipepath)[0]

        print(drink)
        name = list(drink.keys())[0]
        drink['image'] = "/home/grant/Projects/priv/barbados/data/images/queen-christina.jpg"

        altname_index = self.make_altname_index(ingredients)

        ingredient_descriptions = {}

        spec = drink['spec'][0]

        header_ingredients = []
        for ingredient in spec['ingredients']:
            print(ingredient)
            try:
                ingredient_detail = ingredients[ingredient['name']]
            except KeyError:
                try:
                    ingredient_detail = ingredients[altname_index[ingredient['name']]]
                except KeyError:
                    ingredient_detail = None

            if ingredient_detail is None:
                ingredient_descriptions[ingredient['name']] = 'No description available.'
            else:
                ingredient_descriptions[ingredient['name']] = ingredient_detail['description']['short']

            if ingredient_detail and 'generic_name' in ingredient_detail.keys():
                print("WE GOT A GENERIC: %s" % ingredient_detail['generic_name'])
                try:
                    generic = ingredients[ingredient_detail['generic_name']]
                except KeyError:
                    try:
                        generic = ingredients[altname_index[ingredient_detail['generic_name']]]
                    except KeyError:
                        print("KEYERRRORRRRRRRRR")
                        generic = None
                header_ingredients.append(generic)
            else:
                header_ingredients.append(ingredient)

        print("LOL")
        print(header_ingredients)

        content = jt.render(drink=drink, spec=spec, ingredient_descriptions=ingredient_descriptions, header_ingredients=header_ingredients)

        barbados.util.write_file('./output/print.html', content)

        options = {
            'page-height': 152,
            'page-width': 102,
            # 'margin-left': '0.25in',
            # 'margin-right': '0.25in',
            # 'margin-top': '0.25in',
            # 'margin-bottom': '0.25in',
            'margin-left': '0in',
            'margin-right': '0in',
            'margin-top': '0in',
            'margin-bottom': '0in',
        }

        pdfkit.from_string(content, './output/print.pdf', options=options)

    @staticmethod
    def make_altname_index(ingredients):
        altname_index = {}
        for ingredient_name in ingredients.keys():
            if 'alternative_names' in ingredients[ingredient_name].keys():
                for altname in ingredients[ingredient_name]['alternative_names']:
                    altname_index[altname] = ingredient_name

        return altname_index

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Create a new recipe YAML',
                                         usage='drink make <drink-name>')
        parser.add_argument('-r', '--recipe', help='path to recipe yaml',
                            required=True, dest='recipepath')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
