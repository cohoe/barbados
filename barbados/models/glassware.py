from barbados.models.base import BarbadosModel
from sqlalchemy import Column, String, JSON


class GlasswareModel(BarbadosModel):
    __tablename__ = 'glassware'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    description = Column(String)
    images = Column(JSON)

    def __repr__(self):
        return "<Barbados::Models::Glassware[%s]>" % self.slug
