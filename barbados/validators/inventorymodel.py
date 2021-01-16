from barbados.objects.text import Slug
from barbados.models import InventoryModel
from barbados.validators.base import BaseValidator


class InventoryModelValidator(BaseValidator):
    for_class = InventoryModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
        # @TODO this
