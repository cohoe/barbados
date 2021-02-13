from barbados.objects.text import Slug
from barbados.models.construction import ConstructionModel
from barbados.validators.base import BaseValidator


class ConstructionModelValidator(BaseValidator):
    for_class = ConstructionModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
