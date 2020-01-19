#!/usr/bin/env python

import json
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory
from barbados.connectors import RedisConnector
import barbados.config

import json
import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

# result = CocktailModel.query(hash_key="margarita").next()

# c_obj = CocktailFactory.model_to_obj(result)
# print(c_obj)

table_scan_results = CocktailModel.scan(rate_limit=1)
# print(table_scan_results.next().__dict__)

index_scan_results = CocktailModel.name_index.scan(rate_limit=1)
results = [result.attribute_values for result in index_scan_results]
# for result in index_scan_results:
#     results[result.slug] = result.attribute_values
# print(json.dumps(results))

rc = RedisConnector()
# rc.set('cocktail_name_list', json.dumps(results))

print(json.loads(rc.get(barbados.config.cache.cocktail_name_list_key)))