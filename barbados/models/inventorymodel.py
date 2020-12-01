from barbados.models.base import BarbadosModel
from sqlalchemy import Column, JSON, String
from sqlalchemy.dialects.postgresql import UUID


class InventoryModel(BarbadosModel):
    __tablename__ = 'inventories'

    # https://stackoverflow.com/questions/52067058/how-to-autogenerate-uuid-for-postgres-in-python
    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String, nullable=False)
    items = Column(JSON, nullable=False)

    def __repr__(self):
        return "<Barbados::Models::InventoryModel[%s]>" % self.id
