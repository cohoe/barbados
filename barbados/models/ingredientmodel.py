from barbados.models.base import BarbadosModel
from barbados.objects.ingredientkinds import IngredientKinds
from barbados.exceptions import ValidationException
from sqlalchemy import Column, String, or_, ARRAY


class IngredientModel(BarbadosModel):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    parent = Column(String, nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    elements = Column(ARRAY(String), nullable=True)

    @staticmethod
    def get_by_slug(slug):
        return IngredientModel.query.get(slug)

    @staticmethod
    def get_usable_ingredients():
        """
        The or_() does some voodoo magic.
        :return: Result object matching the query.
        """
        expressions = [IngredientModel.kind == kind_class.value for kind_class in IngredientKinds.usables]
        return IngredientModel.query.filter(or_(*expressions))

    @staticmethod
    def get_by_kind(kind):
        """
        Return a list of all ingredients of a particular kind.
        :param kind: Kind class to match against.
        :return: Result object matching the query.
        """
        return IngredientModel.query.filter(IngredientModel.kind == kind.value)

    def validate(self):
        self._check_kind()
        self._check_parent_existence()
        self._check_parent_kind()
        self._check_elements()
        # @TODO check_aliases display_name not in aliases

    def _check_kind(self):
        try:
            kind_class = IngredientKinds(self.kind)
        except KeyError:
            ValidationException("Ingredient %s has bad kind: %s" % (self.slug, self.kind))

    def _check_parent_existence(self):
        if self.kind == IngredientKinds.top.value:
            return

        parent = self._get_parent()
        if not parent:
            raise ValidationException("Parent of %s does not exist (%s)" % (self.slug, self.parent))

    def _check_parent_kind(self):
        parent = self._get_parent()

        if parent is None and IngredientKinds(self.kind) == IngredientKinds.top:
            return

        try:
            if IngredientKinds(parent.kind).value not in IngredientKinds(self.kind).allowed_parents:
                raise ValidationException("Parent (%s) of %s has invalid kind (%s)." % (parent.slug, self.slug, parent.kind))
        except KeyError:
            raise ValidationException("Parent (%s) of %s has bad kind (%s)" % (parent.slug, self.slug, parent.kind))

    def _get_parent(self):
        # https://github.com/sqlalchemy/sqlalchemy/commit/997f4b5f2b3b4725de0960824e95fcb1150ff215
        return self.query.get(self.parent) if self.parent is not None else None

    def _check_elements(self):
        if self.elements:
            if self.kind != IngredientKinds.index.value:
                raise ValidationException("Kind %s of %s cannot have elements." % (self.kind, self.slug))

            for slug in self.elements:
                child = self.query.get(slug)
                if child is None:
                    raise ValidationException("Element %s of %s does not exist." % (slug, self.slug))

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
