from .cocktailmodelvalidator import CocktailModelValidator


class ValidatorFactory:

    def __init__(self):
        self._validators = {}

    def register_class(self, validator):
        class_name = validator.for_class
        self._validators[class_name] = validator

    def get_validator(self, validatable, fatal):
        class_name = validatable.__class__.__name__
        validator = self._validators.get(class_name)
        if not validator:
            raise ValueError(class_name)
        return validator(validatable, fatal)


validator_factory = ValidatorFactory()
validator_factory.register_class(CocktailModelValidator)


class ObjectValidator:
    """
    https://realpython.com/factory-method-python/
    """
    @staticmethod
    def validate(input_object, fatal=True):
        validator = validator_factory.get_validator(input_object, fatal)
        validator.validate()
