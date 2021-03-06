from barbados.validators.cocktailmodel import CocktailModelValidator
from barbados.validators.ingredientmodel import IngredientModelValidator
from barbados.validators.drinklistmodel import DrinkListModelValidator
from barbados.validators.inventorymodel import InventoryModelValidator


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
            raise ValueError("No validator found for %s." % class_name)
        return validator(validatable, fatal)


validator_factory = ValidatorFactory()
validator_factory.register_class(CocktailModelValidator)
validator_factory.register_class(IngredientModelValidator)
validator_factory.register_class(DrinkListModelValidator)
validator_factory.register_class(InventoryModelValidator)


class ObjectValidator:
    """
    https://realpython.com/factory-method-python/
    """
    @staticmethod
    def validate(input_object, session, fatal=True):
        """
        This provides a generic method to call with any object and magically
        find its validator and run the validate() method.
        :param input_object: Object to validate.
        :param session: Database session.
        :param fatal: Whether validation should trigger a fatal exception or not.
        :return: None
        """
        validator = validator_factory.get_validator(input_object, fatal)
        validator.validate(session)
