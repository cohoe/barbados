from barbados.exceptions import ValidationException
from barbados.services.logging import Log


class BaseValidator:

    def fail(self, message):
        Log.error(message)
        if self.fatal:
            raise ValidationException(message)

    def validate(self, session):
        raise NotImplementedError

    @property
    def for_class(self):
        raise NotImplementedError
