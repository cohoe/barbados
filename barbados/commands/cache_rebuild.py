import argparse
import sys
import barbados.config
import json
from barbados.connectors import PostgresqlConnector, RedisConnector
from barbados.models import CocktailModel, IngredientModel
from barbados.objects.ingredient import IngredientTypeEnum
from sqlalchemy import or_


class CacheRebuild:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        redis = RedisConnector()
        conn = PostgresqlConnector()
        sess = conn.Session()

        self._build_cocktail_cache(sess, redis)
        self._build_ingredient_cache(sess, redis)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Rebuild cache',
                                         usage='drink cache-rebuild')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass

    @staticmethod
    def _build_cocktail_cache(sess, redis):
        # This is still returning all values, just not populating them
        scan_results = sess.query(CocktailModel).add_columns(CocktailModel.slug, CocktailModel.display_name).all()

        index = {}
        for result in scan_results:
            key_alpha = result.slug[0].upper()
            key_entry = {
                'slug': result.slug,
                'display_name': result.display_name
            }
            if key_alpha not in index.keys():
                index[key_alpha] = [key_entry]
            else:
                index[key_alpha].append(key_entry)

        redis.set(barbados.config.cache.cocktail_name_list_key, json.dumps(index))

    @staticmethod
    def _build_ingredient_cache(sess, redis):
        # This is still returning all values, just not populating them
        scan_results = sess.query(IngredientModel).add_columns(IngredientModel.slug, IngredientModel.display_name).filter(or_(IngredientModel.type == IngredientTypeEnum.INGREDIENT.value, IngredientModel.type == IngredientTypeEnum.FAMILY.value))

        index = []
        for result in scan_results:
            index.append({
                'slug': result.slug,
                'display_name': result.display_name
            })

        redis.set(barbados.config.cache.ingredient_name_list_key, json.dumps(index))