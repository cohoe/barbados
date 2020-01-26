import argparse
import sys
import barbados.util
from barbados.models import CocktailModel, IngredientModel
from barbados.factories import CocktailFactory
from barbados.connectors import PostgresqlConnector
from barbados.objects import Ingredient
from barbados.constants import IngredientTypeEnum


class Import:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        conn = PostgresqlConnector()
        sess = conn.Session()

        if args.object == 'recipe':
            c = CocktailFactory.obj_from_file(args.recipepath)
            print("Working %s" % args.recipepath)

            print(c.serialize())

            # @TODO upsert or at least deal with re-import
            db_obj = CocktailModel(**c.serialize())
            conn.save(db_obj)
        elif args.object == 'ingredients':
            data = barbados.util.read_yaml_file(args.filepath)

            # Drop the data and reload
            print("deleting old data")
            deleted = sess.query(IngredientModel).delete()
            sess.commit()
            print(deleted)

            print("starting import")
            for ingredient in data:
                i = Ingredient(**ingredient)
                db_obj = IngredientModel(**i.serialize())

                # Test for existing
                existing = sess.query(IngredientModel).get(i.slug)
                if existing:
                    if existing.type == IngredientTypeEnum.CATEGORY.value or existing.type == IngredientTypeEnum.FAMILY.value:
                        if i.type_ is IngredientTypeEnum.INGREDIENT:
                            print("Skipping %s (t:%s) since a broader entry exists (%s)" % (i.slug, i.type_.value, existing.type))
                        else:
                            print("%s (p:%s) already exists as a %s (p:%s)" % (i.slug, i.parent, existing.type, existing.parent))
                    else:
                        print("%s (p:%s) already exists as a %s (p:%s)" % (i.slug, i.parent, existing.type, existing.parent))
                else:
                    conn.save(db_obj)

            # Validate
            print("starting validation")
            ingredients = sess.query(IngredientModel).all()
            for ingredient in ingredients:
                # find parent
                print(ingredient.parent)
                if not ingredient.parent:
                    continue
                parent = sess.query(IngredientModel).get(ingredient.parent)
                if not parent:
                    print("Could not find parent %s for %s" % (ingredient.parent, ingredient.slug))
        else:
            exit(1)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Import something to the database',
                                         usage='drink import <object> <recipepath>')
        parser.add_argument('object', help='object to import', choices=['recipe', 'ingredients'])
        parser.add_argument('filepath', help='path to the yaml file containing the objects')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
