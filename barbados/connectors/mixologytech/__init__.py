from barbados.services.logging import logging
from barbados.connectors.sqlite import SqliteConnector
from barbados.objects.ingredientkinds import IngredientKind, ProductKind
from barbados.text import Slug, DisplayName
from barbados.models.mixologytech import IngredientModel, IngredientAlternateSpellingModel, IngredientSynonymModel
from barbados.models.mixologytech import IngredientCategoryMappingModel, IngredientCategoryModel


class MixologyTechConnector:
    def __init__(self, database_path):
        self.dbconn = SqliteConnector(path=database_path)

    def get_ingredients(self):
        all_ingredients = IngredientModel.query.all()
        # logging.info("Total ingredient count is %i" % len(all_ingredients))

        standardized_ingredients = []
        orphan_count = 0
        for ingredient in all_ingredients:
            # logging.info("Parsing %s" % ingredient.canonical_name)

            parent = self._get_parent_name(ingredient)
            if parent:
                kind = ProductKind.value
            else:
                kind = IngredientKind.value
                orphan_count += 1
            # logging.info("Parent is %s" % parent)

            standardized_ingredient = {
                'display_name': ingredient.canonical_name,
                'slug': Slug(ingredient.canonical_name),
                'aliases': self._get_ingredient_aliases(ingredient),
                'parent': parent,
                'kind': kind,
            }

            standardized_ingredients.append(standardized_ingredient)
            logging.info(standardized_ingredient) if not standardized_ingredient['parent'] else None

        # print(len(IngredientModel.query.all()))
        # for ingredient in IngredientModel.query.all():
            # print(ingredient.canonical_name)
        # for altname in IngredientAlternateSpellingModel.query.all():
            # print(altname.ingredient_id)
        logging.info("Orphans at %i" % orphan_count)
        return standardized_ingredients

    @staticmethod
    def _get_ingredient_aliases(ingredient):
        spellings = IngredientAlternateSpellingModel.query.filter(IngredientAlternateSpellingModel.ingredient_id == ingredient.id)
        synonyms = IngredientSynonymModel.query.filter(IngredientSynonymModel.ingredient_id == ingredient.id)
        aliases = [spelling.alternative_spelling for spelling in spellings] + [synonym.synonym for synonym in synonyms]
        # logging.info("Ingredient %s as %i alias(es)." % (ingredient.canonical_name, len(aliases)))
        return aliases

    @staticmethod
    def _get_parent_name(ingredient):
        if not ingredient.generic_id:
            return MixologyTechConnector._get_ingredient_primary_category(ingredient)

        return IngredientModel.query.get(ingredient.generic_id).canonical_name

    @staticmethod
    def _get_ingredient_primary_category(ingredient):
        category_mappings = IngredientCategoryMappingModel.query.filter(IngredientCategoryMappingModel.ingredient_id == ingredient.id)
        # print([mapping.category_id for mapping in category_mappings])
        # exit()
        for category_id in [result.category_id for result in category_mappings]:
            category = IngredientCategoryModel.query.get(category_id)
            if category.position and category.position >= 5:
                return category.display_name

        logging.error("Could not find category for %s" % ingredient.canonical_name)