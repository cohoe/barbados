from barbados.objects.text import Slug
from barbados.models import IngredientModel
from barbados.validators.base import BaseValidator
from barbados.objects.ingredientkinds import IngredientKinds
from barbados.exceptions import ValidationException


class IngredientModelValidator(BaseValidator):
    for_class = IngredientModel

    def __init__(self, model, fatal=True):
        self.model = model
        self.fatal = fatal
        self.session = None

    def validate(self, session):
        self.session = session

        self._check_kind()
        self._check_parent_existence()
        self._check_parent_kind()
        self._check_elements()
        self._check_slug()
        # @TODO check_aliases display_name not in aliases

    def _check_kind(self):
        try:
            kind_class = IngredientKinds(self.model.kind)
        except KeyError:
            ValidationException("Ingredient %s has bad kind: %s" % (self.model.slug, self.model.kind))

    def _check_parent_existence(self):
        if self.model.kind == IngredientKinds.top.value:
            return

        parent = self._get_parent()
        if not parent:
            raise ValidationException("Parent of %s does not exist (%s)" % (self.model.slug, self.model.parent))

    def _check_parent_kind(self):
        parent = self._get_parent()

        if parent is None and IngredientKinds(self.model.kind) == IngredientKinds.top:
            return

        try:
            if IngredientKinds(parent.kind).value not in IngredientKinds(self.model.kind).allowed_parents:
                raise ValidationException("Parent (%s) of %s has invalid kind (%s)." % (parent.slug, self.model.slug, parent.kind))
        except KeyError:
            raise ValidationException("Parent (%s) of %s has bad kind (%s)" % (parent.slug, self.model.slug, parent.kind))

    def _get_parent(self):
        # https://github.com/sqlalchemy/sqlalchemy/commit/997f4b5f2b3b4725de0960824e95fcb1150ff215
        return self.session.query(IngredientModel).get(self.model.parent) if self.model.parent is not None else None

    def _check_elements(self):
        if self.model.elements:
            if self.model.kind != IngredientKinds.index.value:
                raise ValidationException("Kind %s of %s cannot have elements." % (self.model.kind, self.model.slug))

            for slug in self.model.elements:
                child = self.session.query(IngredientModel).get(slug)
                if child is None:
                    raise ValidationException("Element %s of %s does not exist." % (slug, self.model.slug))

    def _check_slug(self):
        if self.model.slug != Slug(self.model.display_name):
            raise ValidationException("Slug (%s) is inconsistent with display_name." % self.model.slug)