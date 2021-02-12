from barbados.models.base import BarbadosModel
from sqlalchemy import Column, String, JSON


class ConstructionModel(BarbadosModel):
    __tablename__ = 'constructions'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    default_instructions = Column(JSON)

    def __repr__(self):
        return "<Barbados::Models::Construction[%s]>" % self.slug
