from barbados.validators.base import BaseValidator
from barbados.models.ingredient import IngredientModel
from barbados.models.inventory import InventoryModel


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
            self._test_model_exists(IngredientModel, item)
