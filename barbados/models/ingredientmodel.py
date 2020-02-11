from barbados.models.base import BarbadosModel
from barbados.constants import IngredientKind, FamilyKind, ProductKind, IngredientKinds, CustomKind
from barbados.exceptions import ValidationException
from sqlalchemy import Column, String, or_


class IngredientModel(BarbadosModel):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    # @TODO figure this out in a sane expandable way
    @staticmethod
    def get_usable_ingredients():
        return IngredientModel.query.add_columns(IngredientModel.slug, IngredientModel.display_name).filter(
            or_(IngredientModel.kind == IngredientKind.value, IngredientModel.kind == FamilyKind.value,
                IngredientModel.kind == ProductKind.value, IngredientModel.kind == CustomKind.value))

    @staticmethod
    def get_by_kind(kind):
        return IngredientModel.query.filter(IngredientModel.kind == kind.value)

    def validate(self):
        self._check_kind()
        self._check_parent_existence()
        self._check_parent_kind()

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
            raise ValidationException("Parent (%s) of %s has bad kind (%s)"% (parent.slug, self.slug, parent.kind))

    def _get_parent(self):
        return self.query.get(self.parent)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
