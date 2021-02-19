from barbados.models.base import BarbadosModel
from sqlalchemy import Column, JSON, String
from sqlalchemy.dialects.postgresql import UUID


class ListModel(BarbadosModel):
    __tablename__ = 'lists'

    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(String, nullable=False)
    items = Column(JSON, nullable=False)
    # @TODO notes?

    def __repr__(self):
        return "<Barbados::Models::ListModel[%s]>" % self.id
