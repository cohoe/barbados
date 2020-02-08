from barbados.models.base import BarbadosModel
from barbados.constants import IngredientKinds, TopIngredientKind
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
            or_(IngredientModel.kind == IngredientKinds.INGREDIENT.value, IngredientModel.kind == IngredientKinds.FAMILY.value,
                IngredientModel.kind == IngredientKinds.PRODUCT.value))

    @staticmethod
    def get_by_kind(kind):
        return IngredientModel.query.filter(IngredientModel.kind == kind.value)

    def validate(self):
        self._check_parent_existence()

    def _check_parent_existence(self):
        if self.kind == TopIngredientKind.value:
            return

        parent = self.query.get(self.parent)
        if not parent:
            raise ValidationException("Parent of %s does not exist (%s)" % (self.slug, self.parent))

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
