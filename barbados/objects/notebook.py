from barbados.services.database import DatabaseService
from barbados.models.cocktail import CocktailModel
from barbados.factories.cocktail import CocktailFactory


class Notebook:
    """
    The Notebook is a list of all Text objects in the
    cocktails/recipes table.
    """
    def __init__(self):
        self.notes = self._get_notes()

    @staticmethod
    def _get_notes():
        """
        Get a list of all notes in the database.
        :return: List[Text]
        """
        notes = []
        with DatabaseService.get_session() as session:
            results = session.query(CocktailModel).all()
            for result in results:
                c = CocktailFactory.model_to_obj(model=result)
                notes += c.notes

                for spec in c.specs:
                    notes += spec.notes

        return notes
