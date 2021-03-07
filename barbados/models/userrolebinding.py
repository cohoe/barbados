from barbados.models.base import BarbadosModel
from sqlalchemy import Column, Integer, ForeignKey


# https://flask-security-too.readthedocs.io/en/stable/quickstart.html#basic-sqlalchemy-application-with-session
class UserRoleBindingModel(BarbadosModel):
    __tablename__ = 'user_role_bindings'

    # id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))

    def __repr__(self):
        return "<Barbados::Models::UserModel[%s]>" % self.id
