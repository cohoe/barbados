from barbados.models.base import Base
from barbados.constants import IngredientTypes
from sqlalchemy import Column, String, or_


class IngredientModel(Base):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    @staticmethod
    def get_usable_ingredients(session):
        return session.query(IngredientModel).add_columns(IngredientModel.slug, IngredientModel.display_name).filter(
            or_(IngredientModel.type == IngredientTypes.INGREDIENT.value, IngredientModel.type == IngredientTypes.FAMILY.value))

    @staticmethod
    def get_by_type(session, type_):
        return session.query(IngredientModel).filter(IngredientModel.type == type_.value)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
