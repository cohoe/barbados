from barbados.objects.text import Slug
from barbados.models.ingredient import IngredientModel
from barbados.validators.base import BaseValidator
from barbados.objects.ingredientkinds import IngredientKinds, CustomKind
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
        self._check_conditions()
        self._check_instructions()
        self._check_components()
        self._check_aliases()

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
        if not self.model.elements_include:
            return

        # Only indexes can have elements
        if self.model.kind != IngredientKinds.index.value:
            raise ValidationException("Kind %s of %s cannot have elements." % (self.model.kind, self.model.slug))

        # If this is at the top if sets off a chain reaction of circular imports.
        # If we load it here then everything has already been initialized and it
        # is safe to do so.
        from barbados.caches.ingredienttree import IngredientTreeCache
        tree = IngredientTreeCache.retrieve()

        for element_slug in self.model.elements_include:
            # Ensure that all elements exist
            child = self.session.query(IngredientModel).get(element_slug)
            if child is None:
                raise ValidationException("Element %s of %s does not exist." % (element_slug, self.model.slug))

            # Elements must have a common family ancestor or
            # be implied by the parents.
            allowed_parents = tree.implies(element_slug) + tree.parents(element_slug)
            if self.model.parent not in allowed_parents and element_slug not in allowed_parents:
                raise ValidationException("Element '%s' of '%s' must have a common implied parent." % (element_slug, self.model.slug))

    def _check_conditions(self):
        if self.model.conditions:
            if self.model.kind != IngredientKinds.index.value:
                raise ValidationException("Kind %s of %s cannot have conditions." % (self.model.kind, self.model.slug))

    def _check_slug(self):
        if self.model.slug != Slug(self.model.display_name):
            raise ValidationException("Slug (%s) is inconsistent with display_name." % self.model.slug)

    def _check_components(self):
        if not self.model.components:
            return
        # Only custom can have components
        if self.model.kind != CustomKind.value:
            raise ValidationException("Kind %s of %s cannot have components." % (self.model.kind, self.model.slug))

    def _check_instructions(self):
        if not self.model.instructions:
            return
        # Only custom can have instructions
        if self.model.kind != CustomKind.value:
            raise ValidationException("Kind %s of %s cannot have instructions." % (self.model.kind, self.model.slug))

    def _check_aliases(self):
        if not self.model.aliases:
            return
        # Ensure display_name isnt in the aliases
        if self.model.display_name in self.model.aliases:
            raise ValidationException("Display Name %s cannot be an alias." % self.model.display_name)
