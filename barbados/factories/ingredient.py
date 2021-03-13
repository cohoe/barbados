import barbados.factories.component
from barbados.objects.ingredient import Ingredient
from barbados.factories.base import BaseFactory
from barbados.models.ingredient import IngredientModel
from barbados.query import QueryCondition
from barbados.validators.ingredientmodel import IngredientModelValidator
from barbados.indexes.ingredient import IngredientIndex
from barbados.objects.text import DisplayName
from barbados.factories.parser import FactoryParser
from barbados.factories.text import TextFactory


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
        'components': list(),
        'instructions': list()
    }

    @classmethod
    def raw_to_obj(cls, input_object):
        raw_ingredient = cls.sanitize_raw(raw_input=input_object, required_keys=cls.required_keys)

        # Beware the Python dict copying bullshit!
        raw_ingredient = cls._parse_conditions(raw_ingredient)
        raw_ingredient = cls._parse_aliases(raw_ingredient)
        raw_ingredient = FactoryParser.parse_display_name(raw_ingredient)
        raw_ingredient = FactoryParser.parse_object_list(raw_ingredient, TextFactory, 'instructions')
        raw_ingredient = FactoryParser.parse_object_list(raw_ingredient, barbados.factories.component.ComponentFactory, 'components')

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
