from barbados.objects.ingredient import Ingredient
from .base import BaseFactory


class IngredientFactory(BaseFactory):

    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(input_object):
        return Ingredient(**input_object)
