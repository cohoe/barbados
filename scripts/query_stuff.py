#!/usr/bin/env python

from barbados.models import CocktailModel
from barbados.factories import CocktailFactory

import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

result = CocktailModel.query(hash_key="margarita").next()

c_obj = CocktailFactory.model_to_obj(result)
print(c_obj)