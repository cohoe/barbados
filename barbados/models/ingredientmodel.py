from barbados.models.base import Base
from sqlalchemy import Column, String


class IngredientModel(Base):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
