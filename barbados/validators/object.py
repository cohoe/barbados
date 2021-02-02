from barbados.validators import validator_factory


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