import argparse
import sys
import barbados.config
import json
from barbados.connectors import PostgresqlConnector, RedisConnector
from barbados.models import CocktailModel


class CacheRebuild:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        redis = RedisConnector()
        conn = PostgresqlConnector()
        sess = conn.Session()

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
    def _setup_args():
        parser = argparse.ArgumentParser(description='Rebuild cache',
                                         usage='drink cache-rebuild')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
