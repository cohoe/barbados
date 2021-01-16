from barbados.models.base import BarbadosModel
from barbados.objects.ingredientkinds import IngredientKinds
from sqlalchemy import Column, String, or_, ARRAY


class IngredientModel(BarbadosModel):
    __tablename__ = 'ingredients'

    slug = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    # At some point, we can turn on ForeignKey('ingredients.slug'). But the import
    # is not smart enough to do creation in order (it just searches for files in
    # the repo).
    parent = Column(String, nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    elements = Column(ARRAY(String), nullable=True)

    @staticmethod
    def get_usable_ingredients(session):
        """
        The or_() does some voodoo magic.
        :return: Result object matching the query.
        """
        expressions = [IngredientModel.kind == kind_class.value for kind_class in IngredientKinds.usables]
        return session.query(IngredientModel).filter(or_(*expressions))

    @staticmethod
    def get_by_kind(session, kind):
        """
        Return a list of all ingredients of a particular kind.
        :param kind: Kind class to match against.
        :return: Result object matching the query.
        """
        return session.query(IngredientModel).filter(IngredientModel.kind == kind.value)

    def __repr__(self):
        return "<Barbados::Models::IngredientModel[%s]>" % self.slug
