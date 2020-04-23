from barbados.objects.ingredient import Ingredient
from .base import BaseFactory


class IngredientFactory(BaseFactory):
    def __init__(self):
        pass

    @staticmethod
    def to_obj(input_object):
        return Ingredient(**input_object)

    @staticmethod
    def model_to_obj(model):
        """
        This exists to ensure common functionality with CocktailModel.
        :param model:
        :return:
        """
        model_dict = model.__dict__
        model_dict.pop('_sa_instance_state')

        return IngredientFactory.to_obj(model_dict)
