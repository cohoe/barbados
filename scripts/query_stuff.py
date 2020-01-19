#!/usr/bin/env python

from barbados.models import CocktailModel

import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

results = CocktailModel.query(hash_key="flor-de-jerez", attributes_to_get=['display_name', 'status', 'notes'])

for result in results:
    print(result.notes)