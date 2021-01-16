from barbados.exceptions import ValidationException
from barbados.services.logging import LogService


class BaseValidator:

    def fail(self, message):
        LogService.error(message)
        if self.fatal:
            raise ValidationException(message)

    def validate(self, session):
        raise NotImplementedError

    @property
    def for_class(self):
        raise NotImplementedError
