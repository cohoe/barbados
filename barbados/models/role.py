from barbados.models.base import BarbadosModel
from sqlalchemy import Column, String, Integer
from flask_security import RoleMixin


# https://flask-security-too.readthedocs.io/en/stable/quickstart.html#basic-sqlalchemy-application-with-session
class RoleModel(BarbadosModel, RoleMixin):
    __tablename__ = 'roles'

    # id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return "<Barbados::Models::RoleModel[%s]>" % self.id
