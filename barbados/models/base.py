from sqlalchemy.ext.declarative import declarative_base

# "Declarative" is this voodoo system of mapping models to tables.
# The "Base" is the catalog of mappings (models). This enables the whole create_all() stuff.
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
#
# The real MVP:
# https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html


class Base:
    pass


BarbadosModel = declarative_base(cls=Base)
# BarbadosModel.query = session.query_property()
MixologyTechModel = declarative_base(cls=Base)
# MixologyTechModel.query = session.query_property()
