import argparse
import sys
import barbados.util
from barbados.objects import Cocktail, Spec, Status, Citation, Text, Origin, Glassware, SpecIngredient


class Migrate:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        try:
            raw_recipe = barbados.util.read_yaml_file(args.recipepath)[0]
        except KeyError as ke:
            self._migrate(args)
            return

        barbados.util.die("This recipe does not smell in need of migration")

    @staticmethod
    def _migrate(args):
        old_recipe = barbados.util.read_yaml_file(args.recipepath)

        drink_name = next(iter(old_recipe.keys()))

        old_recipe = old_recipe[drink_name]
        # print(old_recipe)

        status_obj = Status(color=old_recipe['status'])

        origin_obj = Origin()
        if 'origin' in old_recipe.keys():
            if old_recipe['origin'] is not None:
                origin_obj = Origin(**old_recipe['origin'])

        ingredient_obj_list = []
        for raw_ingredient in old_recipe['ingredients']:
            spec_ing_obj = SpecIngredient(**raw_ingredient)
            ingredient_obj_list.append(spec_ing_obj)

        citation_obj_list = []
        if 'sources' in old_recipe.keys():
            if old_recipe['sources'] is not None:
                for raw_citation in old_recipe['sources']:
                    keys = {}

                    if 'name' in raw_citation:
                        keys['title'] = raw_citation['name']
                    if 'page' in raw_citation:
                        keys['page'] = raw_citation['page']
                    if 'href' in raw_citation:
                        keys['href'] = raw_citation['href']
                    if 'issue' in raw_citation:
                        keys['issue'] = raw_citation['issue']
                    if 'year' in raw_citation:
                        keys['date'] = raw_citation['year']

                    citation_obj = Citation(**keys)
                    citation_obj_list.append(citation_obj)

        notes_objs = []
        if 'notes' in old_recipe.keys():
            if old_recipe['notes'] is not None:
                for note in old_recipe['notes']:
                    note_obj = Text(text=note)
                    notes_objs.append(note_obj)

        garnish_objs = []
        if 'garnish' in old_recipe.keys():
            if old_recipe['garnish'] is not None:
                for garnish in old_recipe['garnish']:
                    garnish_obj = SpecIngredient(name=garnish)
                    garnish_objs.append(garnish_obj)

        instructions_obj = []
        for instruction in old_recipe['instructions']:
            instr_obj = Text(text=instruction)
            instructions_obj.append(instr_obj)

        glassware = Glassware()
        if 'glassware' in old_recipe.keys():
            if old_recipe['glassware'] is not None:
                glassware = Glassware(name=old_recipe['glassware'])

        spec_obj = Spec(name='Original',
                        origin=origin_obj,
                        glassware=glassware,
                        ingredients=ingredient_obj_list,
                        citations=citation_obj_list,
                        notes=notes_objs,
                        straw=None,
                        garnish=garnish_objs,
                        instructions=instructions_obj
                        )

        # print(spec_obj)

        c_obj = Cocktail(name=drink_name,
                         status=status_obj,
                         origin=origin_obj,
                         specs=[spec_obj],
                         citations=None,
                         notes=None,
                         tags=None
                         )

        jt = barbados.util.load_template_from_file('./templates/migration.yaml')

        content = jt.render(cocktail=c_obj, spec=spec_obj)
        print(content)

        barbados.util.write_file(args.recipepath, content)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Print a cocktail object',
                                         usage='drink testcmd <recipepath>')
        parser.add_argument('recipepath', help='path to recipe yaml')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
