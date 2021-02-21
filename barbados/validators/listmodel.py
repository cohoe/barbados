from barbados.models.cocktail import CocktailModel
from barbados.models.list import ListModel
from barbados.validators.base import BaseValidator
from barbados.exceptions import ValidationException
from uuid import UUID


class ListModelValidator(BaseValidator):
    for_class = ListModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session
        self._check_id()
        self._check_items()

    def _check_id(self):
        try:
            uuid = UUID(self.model.id)
        except ValueError as e:
            raise ValidationException(e)

    def _check_items(self):
        for item in self.model.items:
            cocktail_slug = item.get('cocktail_slug')
            c_db = self.session.query(CocktailModel).get(cocktail_slug)
            if not c_db:
                self.fail("Cocktail slug %s does not exist." % cocktail_slug)

            spec_slug = item.get('spec_slug')
            if spec_slug:
                c_spec_slugs = [spec.get('slug') for spec in c_db.specs]
                if spec_slug not in c_spec_slugs:
                    self.fail("Spec slug %s does not exist for %s." % (spec_slug, cocktail_slug))
