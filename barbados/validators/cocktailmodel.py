from barbados.objects.text import Slug
from barbados.models.ingredient import IngredientModel
from barbados.models.construction import ConstructionModel
from barbados.models.glassware import GlasswareModel
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
            # Components
            for component in spec.get('components'):
                self._test_model_exists(IngredientModel, component.get('slug'))
            # Garnish
            for garnish in spec.get('garnish'):
                self._test_model_exists(IngredientModel, garnish.get('slug'))
            # Construction
            self._test_model_exists(ConstructionModel, spec.get('construction').get('slug'))
            # Glassware
            for glassware in spec.get('glassware'):
                self._test_model_exists(GlasswareModel, glassware.get('slug'))
