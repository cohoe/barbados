#!/usr/bin/env python

from barbados.models import CocktailModel

import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

if not CocktailModel.exists():
    CocktailModel.create_table(wait=True)

spec = [
    {
        'name': 'spec 1',
        'ingredients': [
            {'name': 'rum'},
            {'name': 'lime'},
            {'name': 'sugar'}
        ]
    },
    {
        'name': 'spec 2',
    }
]

cocktail = CocktailModel(slug="slugy-mcslugface", display_name="Sluggy McSlugface", spec=spec, status='green', spec_count=len(spec))
cocktail.save()

from barbados.factories import CocktailFactory

c = CocktailFactory.obj_from_file('../../tortuga/recipes/flor-de-jerez.yaml')

blob = c.serialize()
print(blob)

# Legacy convertion
name = blob.pop('name', None)
blob['display_name'] = name

c2 = CocktailModel(**blob)
c2.save()

# @TODO
# * spec -> specs
# * name -> display_name
# * slug
