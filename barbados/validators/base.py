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

    def _test_model_exists(self, model, slug):
        m = self.session.query(model).get(slug)
        if not m:
            self.fail("%s %s does not exist." % (model, slug))
