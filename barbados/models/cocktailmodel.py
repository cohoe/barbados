from barbados.models.base import Base
from sqlalchemy import Column, Integer, JSON, String


class CocktailModel(Base):
    __tablename__ = 'cocktails'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    specs = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    citations = Column(JSON, nullable=True)
    notes = Column(JSON, nullable=True)
    origin = Column(JSON, nullable=False)
    spec_count = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Barbaros::Models::CocktailModel[%s]>" % self.slug