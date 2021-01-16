from barbados.models.base import BarbadosModel
from sqlalchemy import Column, JSON, String


class MenuModel(BarbadosModel):
    __tablename__ = 'menus'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    items = Column(JSON, nullable=False)

    def __repr__(self):
        return "<Barbados::Models::MenuModel[%s]>" % self.slug
