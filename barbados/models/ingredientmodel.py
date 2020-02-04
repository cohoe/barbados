from barbados.models.base import Base
from barbados.constants import IngredientTypes
from sqlalchemy import Column, String, or_



class IngredientModel(Base):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    def __init__(self, session):
        self.session = session

    def get_usable_ingredients(self):
        return self.session.query(IngredientModel).add_columns(IngredientModel.slug, IngredientModel.display_name).filter(
            or_(IngredientModel.type == IngredientTypes.INGREDIENT.value, IngredientModel.type == IngredientTypes.FAMILY.value))

    def get_by_type(self, type):
        return self.session.query(IngredientModel).filter(IngredientModel.type == type.value)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
