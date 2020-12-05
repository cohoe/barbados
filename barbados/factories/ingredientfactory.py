from barbados.objects.ingredient import Ingredient
from .base import BaseFactory
from barbados.models.ingredientmodel import IngredientModel


class IngredientFactory(BaseFactory):
    _model = IngredientModel

    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(input_object):
        return Ingredient(**input_object)
