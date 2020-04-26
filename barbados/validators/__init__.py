from .cocktailmodelvalidator import CocktailModelValidator
from .ingredientmodelvalidator import IngredientModelValidator


class ValidatorFactory:

    def __init__(self):
        self._validators = {}

    def register_class(self, validator):
        class_name = validator.for_class
        self._validators[class_name] = validator

    def get_validator(self, validatable, fatal):
        class_name = validatable.__class__
        validator = self._validators.get(class_name)
        if not validator:
            raise ValueError(class_name)
        return validator(validatable, fatal)


# @TODO can these go back to their individual classes?
validator_factory = ValidatorFactory()
validator_factory.register_class(CocktailModelValidator)
validator_factory.register_class(IngredientModelValidator)


class ObjectValidator:
    """
    https://realpython.com/factory-method-python/
    """
    @staticmethod
    def validate(input_object, session, fatal=True):
        validator = validator_factory.get_validator(input_object, fatal)
        validator.validate(session)
