from barbados.services.registry import RegistryService
from barbados.models.cocktail import CocktailModel
from barbados.factories.cocktailfactory import CocktailFactory


class Bibliography:
    """
    The Bibliography is a list of all Citation objects in the
    cocktails/recipes table.
    """
    def __init__(self):
        self.citations = self._get_citations()

    @staticmethod
    def _get_citations():
        """
        Get a list of all citations in the database.
        :return: List[Citation]
        """
        citations = []
        pgconn = RegistryService.get_database_connection()
        with pgconn.get_session() as session:
            results = session.query(CocktailModel).all()
            for result in results:
                c = CocktailFactory.model_to_obj(model=result)
                # Recipe-specific citations
                citations += c.citations

                for spec in c.specs:
                    citations += spec.citations

        return citations
