import logging
from barbados.exceptions import ValidationException


class BaseValidator:

    def fail(self, message):
        logging.error(message)
        if self.fatal:
            raise ValidationException(message)