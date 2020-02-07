from barbados.models.base import BarbadosModel
from barbados.constants import IngredientTypes
from sqlalchemy import Column, String, or_


class IngredientModel(BarbadosModel):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    @staticmethod
    def get_usable_ingredients():
        return IngredientModel.query.add_columns(IngredientModel.slug, IngredientModel.display_name).filter(
            or_(IngredientModel.type == IngredientTypes.INGREDIENT.value, IngredientModel.type == IngredientTypes.FAMILY.value))

    @staticmethod
    def get_by_type(type_):
        return IngredientModel.query.filter(IngredientModel.type == type_.value)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
