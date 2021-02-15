from barbados.objects.text import Slug
from barbados.models.ingredient import IngredientModel
from barbados.models.cocktail import CocktailModel
from barbados.validators.base import BaseValidator


class CocktailModelValidator(BaseValidator):
    for_class = CocktailModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
        self._check_slug()
        self._check_spec()

    def _check_slug(self):
        slug = self.model.slug
        calculated_slug = Slug(self.model.display_name)

        if slug != calculated_slug:
            self.fail("Slug (%s) is inconsistent with display_name (%s)." % (self.model.slug, self.model.display_name))

    def _check_spec(self):
        for spec in self.model.specs:
            for component in spec.get('components'):
                self._test_component_exists(component)
            for garnish in spec.get('garnish'):
                self._test_component_exists(garnish)

    def _test_component_exists(self, component):
        component_slug = component['slug']
        i = self.session.query(IngredientModel).get(component_slug)
        if not i:
            self.fail("Ingredient %s does not exist." % component_slug)
