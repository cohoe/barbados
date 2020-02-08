from barbados.models.base import BarbadosModel
from barbados.constants import IngredientKinds
from sqlalchemy import Column, String, or_


class IngredientModel(BarbadosModel):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    @staticmethod
    def get_usable_ingredients():
        return IngredientModel.query.add_columns(IngredientModel.slug, IngredientModel.display_name).filter(
            or_(IngredientModel.kind == IngredientKinds.INGREDIENT.value, IngredientModel.kind == IngredientKinds.FAMILY.value,
                IngredientModel.kind == IngredientKinds.PRODUCT.value))

    @staticmethod
    def get_by_kind(kind):
        return IngredientModel.query.filter(IngredientModel.kind == kind.value)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
