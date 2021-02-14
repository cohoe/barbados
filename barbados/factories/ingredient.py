from barbados.objects.ingredient import Ingredient
from barbados.factories.base import BaseFactory
from barbados.models.ingredient import IngredientModel
from barbados.query import QueryCondition
from barbados.validators.ingredientmodel import IngredientModelValidator
from barbados.indexes.ingredient import IngredientIndex
from barbados.objects.text import DisplayName


class IngredientFactory(BaseFactory):
    _model = IngredientModel
    _validator = IngredientModelValidator
    _index = IngredientIndex

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
        raw_ingredient = IngredientFactory._parse_aliases(raw_ingredient)
        raw_ingredient = IngredientFactory._parse_display_name(raw_ingredient)

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

    @staticmethod
    def _parse_aliases(raw_input):
        key = 'aliases'

        objs = []
        for raw_alias in raw_input.get(key):
            d = DisplayName(raw_alias)
            objs.append(d)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_display_name(raw_input):
        key = 'display_name'
        try:
            d = DisplayName(raw_input[key])
        except KeyError:
            d = DisplayName(raw_input.get('slug'))
        raw_input.update({key: d})
        return raw_input
