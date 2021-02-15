from barbados.objects.text import Slug
from barbados.models.glassware import GlasswareModel
from barbados.validators.base import BaseValidator


class GlasswareModelValidator(BaseValidator):
    for_class = GlasswareModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
