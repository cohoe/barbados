from barbados.objects.text import Slug
from barbados.models.inventory import InventoryModel
from barbados.validators.base import BaseValidator


class InventoryModelValidator(BaseValidator):
    for_class = InventoryModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
        self._check_items()

    def _check_items(self):
        for item in self.model.items:
            self._test_ingredient_exists(item)
