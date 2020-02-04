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

    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(CocktailModel).add_columns(CocktailModel.slug, CocktailModel.display_name).all()

    def get_by_slug(self, slug):
        return self.session.query(CocktailModel).get(slug)

    def __repr__(self):
        return "<Barbados::Models::CocktailModel[%s]>" % self.slug
