from barbados.models.base import BarbadosModel
from sqlalchemy import Column, Integer, JSON, String


class CocktailModel(BarbadosModel):
    __tablename__ = 'cocktails'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    specs = Column(JSON, nullable=False)
    citations = Column(JSON, nullable=True)
    notes = Column(JSON, nullable=True)
    origin = Column(JSON, nullable=False)
    spec_count = Column(Integer, nullable=False)


    @staticmethod
    def get_all():
        return CocktailModel.query.add_columns(CocktailModel.slug, CocktailModel.display_name).all()

    @staticmethod
    def get_by_slug(slug):
        return CocktailModel.query.get(slug)

    def __repr__(self):
        return "<Barbados::Models::CocktailModel[%s]>" % self.slug