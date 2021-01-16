from barbados.objects.text import Slug
from barbados.models import CocktailModel, MenuModel
from barbados.validators.base import BaseValidator


class MenuModelValidator(BaseValidator):
    for_class = MenuModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
        self._check_slug()
        self._check_items()

    def _check_slug(self):
        slug = self.model.slug
        calculated_slug = Slug(self.model.display_name)

        if slug != calculated_slug:
            self.fail("Slug (%s) is inconsistent with display_name (%s)." % (self.model.slug, self.model.display_name))

    def _check_items(self):
        for item in self.model.items:
            cocktail_slug = item.get('cocktail_slug')
            c_db = self.session.query(CocktailModel).get(cocktail_slug)
            if not c_db:
                self.fail("Cocktail slug %s does not exist." % cocktail_slug)

            # @TODO spec slug validation
            spec_slug = item.get('spec_slug')
            if spec_slug:
                c_spec_slugs = [spec.get('slug') for spec in c_db.specs]
                if spec_slug not in c_spec_slugs:
                    self.fail("Spec slug %s does not exist for %s." % (spec_slug, cocktail_slug))
