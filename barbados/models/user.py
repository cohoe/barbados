from barbados.models.base import BarbadosModel
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin


# https://flask-security-too.readthedocs.io/en/stable/quickstart.html#basic-sqlalchemy-application-with-session
class UserModel(BarbadosModel, UserMixin):
    __tablename__ = 'users'

    # id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('RoleModel', secondary='user_role_bindings',
                         backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<Barbados::Models::UserModel[%s]>" % self.id
