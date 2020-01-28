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
            self._import_recipe(args.filepath, conn, sess)
        elif args.object == 'recipes':
            recipe_dir = args.filepath
            for filename in barbados.util.list_files(recipe_dir):
                self._import_recipe("%s/%s" % (recipe_dir, filename), conn, sess)
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
        parser.add_argument('object', help='object to import', choices=['recipe', 'recipes', 'ingredients'])
        parser.add_argument('filepath', help='path to the yaml file (or directory) containing the objects')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass

    @staticmethod
    def _import_recipe(filepath, db_conn, db_sess):
        c = CocktailFactory.obj_from_file(filepath)
        print("Working %s" % filepath)

        # Drop the data and reload
        print("deleting old data")
        # Test for existing
        existing = db_sess.query(CocktailModel).get(c.slug)
        if existing:
            db_sess.delete(existing)
            db_sess.commit()

        db_obj = CocktailModel(**c.serialize())
        db_conn.save(db_obj)
        print("created new")