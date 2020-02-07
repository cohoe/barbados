from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import DatabaseError

session = scoped_session(sessionmaker(autocommit=False))

# The real MVP:
# https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html


class Base(object):

    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    def _flush(self):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


BarbadosModel = declarative_base(cls=Base)
BarbadosModel.query = session.query_property()
