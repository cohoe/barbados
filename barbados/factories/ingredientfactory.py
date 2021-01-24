from barbados.objects.ingredient import Ingredient
from .base import BaseFactory
from barbados.models.ingredient import IngredientModel
from barbados.query import QueryCondition


class IngredientFactory(BaseFactory):
    _model = IngredientModel

    required_keys = {
        'slug': str(),
        'display_name': str(),
        'kind': str(),
        'parent': str(),
        'elements': list(),
        'aliases': list(),
        'conditions': list(),
        'elements_include': list(),
        'elements_exclude': list(),
        'last_refresh': None,
    }

    @staticmethod
    def raw_to_obj(input_object):
        raw_ingredient = IngredientFactory.sanitize_raw(raw_input=input_object, required_keys=IngredientFactory.required_keys)

        # Beware the Python dict copying bullshit!
        raw_ingredient = IngredientFactory._parse_conditions(raw_ingredient)
        # @TODO parse aliases and displayname as displayname objects, among other things.

        # Build the object
        i = Ingredient(**raw_ingredient)
        return i

    @staticmethod
    def _parse_conditions(raw_input):
        raw_input_key = 'conditions'
        conditions = raw_input.get(raw_input_key)

        condition_objects = []
        for raw_condition in conditions:
            qc = QueryCondition(**raw_condition)
            condition_objects.append(qc)

        raw_input.update({raw_input_key: condition_objects})
        return raw_input
