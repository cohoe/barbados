from barbados.models.base import BarbadosModel
from sqlalchemy import Column, JSON, String
from sqlalchemy.dialects.postgresql import UUID


class DrinkListModel(BarbadosModel):
    __tablename__ = 'drinklists'

    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String, nullable=False)
    items = Column(JSON, nullable=False)

    def __repr__(self):
        return "<Barbados::Models::DrinkListModel[%s]>" % self.id
