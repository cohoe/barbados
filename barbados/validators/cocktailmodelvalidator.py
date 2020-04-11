from barbados.text import Slug
from barbados.models import IngredientModel
from .basevalidator import BaseValidator


class CocktailModelValidator(BaseValidator):
    for_class = 'CocktailModel'

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal

    def validate(self):
        self._check_slug()
        self._check_spec()

    def _check_slug(self):
        slug = self.model.slug
        calculated_slug = Slug(self.model.display_name)

        if slug != calculated_slug:
            self.fail("Slug (%s) is inconsistent with display_name (%s)." % (self.model.slug, self.model.display_name))

    def _check_spec(self):
        for spec in self.model.specs:
            for component in spec['components']:
                # It's been serialized at this point
                i = IngredientModel.get_by_slug(component['slug'])
                if not i:
                    self.fail("Ingredient %s does not exist." % component['slug'])