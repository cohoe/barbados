from barbados.services.logging import Log
from barbados.connectors.sqlite import SqliteConnector
from barbados.objects.ingredientkinds import IngredientKind, ProductKind
from barbados.text import Slug, DisplayName
from barbados.models.mixologytech import IngredientModel, IngredientAlternateSpellingModel, IngredientSynonymModel
from barbados.models.mixologytech import IngredientCategoryMappingModel, IngredientCategoryModel
from barbados.models.mixologytech import RecipeModel
from barbados.factories import CocktailFactory
from barbados.serializers import ObjectSerializer
import re


class MixologyTechConnector:
    def __init__(self, database_path):
        self.dbconn = SqliteConnector(path=database_path)

    def get_ingredients(self):
        all_ingredients = IngredientModel.query.all()
        # Log.info("Total ingredient count is %i" % len(all_ingredients))

        standardized_ingredients = []
        orphan_count = 0
        for ingredient in all_ingredients:
            # Log.info("Parsing %s" % ingredient.canonical_name)

            parent = self._get_parent_name(ingredient)
            if parent:
                kind = ProductKind.value
            else:
                kind = IngredientKind.value
                orphan_count += 1
            # Log.info("Parent is %s" % parent)

            standardized_ingredient = {
                'display_name': ingredient.canonical_name,
                'slug': Slug(ingredient.canonical_name),
                'aliases': self._get_ingredient_aliases(ingredient),
                'parent': parent,
                'kind': kind,
            }

            standardized_ingredients.append(standardized_ingredient)
            Log.info(standardized_ingredient) if not standardized_ingredient['parent'] else None

        # print(len(IngredientModel.query.all()))
        # for ingredient in IngredientModel.query.all():
        # print(ingredient.canonical_name)
        # for altname in IngredientAlternateSpellingModel.query.all():
        # print(altname.ingredient_id)
        Log.info("Orphans at %i" % orphan_count)
        return standardized_ingredients

    @staticmethod
    def _get_ingredient_aliases(ingredient):
        spellings = IngredientAlternateSpellingModel.query.filter(IngredientAlternateSpellingModel.ingredient_id == ingredient.id)
        synonyms = IngredientSynonymModel.query.filter(IngredientSynonymModel.ingredient_id == ingredient.id)
        aliases = [spelling.alternative_spelling for spelling in spellings] + [synonym.synonym for synonym in synonyms]
        # Log.info("Ingredient %s as %i alias(es)." % (ingredient.canonical_name, len(aliases)))
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

        Log.error("Could not find category for %s" % ingredient.canonical_name)

    def get_recipes(self):
        with self.dbconn.get_session() as session:
            raw_recipes = session.query(RecipeModel).all()

            objs = []

            for recipe in raw_recipes:
                if not recipe.is_ingredient:
                    objs.append(MixologyTechConnector._model_to_obj(recipe))

            # return [MixologyTechConnector._model_to_obj(raw_recipe) for raw_recipe in raw_recipes]
            return objs

    @staticmethod
    def _model_to_obj(raw_recipe):
        slug = Slug(raw_recipe.title)
        recipe_dict = {
            'display_name': raw_recipe.title,
            'specs': [{
                # 'slug': raw_recipe.presentation,
                'slug': 'pdt',
                'display_name': 'PDT',
                'origin': MixologyTechConnector._get_origin(raw_recipe)
            }]
        }

        recipe_dict['specs'][0].update(MixologyTechConnector._detail_to_spec(raw_recipe.detail_json))

        print(recipe_dict)

        return CocktailFactory.raw_to_obj(raw_recipe=recipe_dict, slug=slug)

    @staticmethod
    def _detail_to_spec(details):
        spec = {
            'notes': [],
            'images': [],
        }
        for detail in details:
            if detail.get('kind') == 'measures':
                spec['components'] = MixologyTechConnector._get_components(detail.get('text'))
            elif detail.get('kind') == 'instructions':
                spec['instructions'] = MixologyTechConnector._get_instructions(detail)
                spec['construction'] = MixologyTechConnector._get_construction(spec.get('instructions'))
                spec['glassware'] = MixologyTechConnector._get_glassware(spec.get('instructions'))
                spec['straw'] = MixologyTechConnector._get_straw(spec.get('instructions'))
            elif detail.get('kind') == 'notes':
                spec['notes'].append(MixologyTechConnector._parse_note(detail.get('text')))
            elif detail.get('kind') == 'graphic':
                pass
            elif detail.get('kind') == 'art':
                pass
            else:
                raise Exception("Unknown detail kind %s" % detail.get('kind'))

        return spec

    @staticmethod
    def _get_instructions(detail):
        instructions = []
        lines = detail.get('text').split('\n')
        for line in lines:
            if line.lower().startswith('garnish'):
                pass
            else:
                instructions.append({'text': line})

        return instructions

    @staticmethod
    def _get_construction(texts):
        for text in texts:
            terms = ['shake', 'stir']
            for term in terms:
                if term in text.get('text').lower():
                    return term

        return 'unknown'

    @staticmethod
    def _parse_note(text):
        text = text.replace('—', '')

        return {'text': text}

    @staticmethod
    def _get_components(text):
        components = []

        lines = text.split('\n')
        for line in lines:
            tokens = re.split(r"([\.\d+]+) ([\w\.]+) (.*)$", line)
            for token in tokens:
                if not token:
                    tokens.remove(token)

            if len(tokens) == 3:
                # quantity, unit, ingredient
                try:
                    quantity = float(tokens[0])
                    if quantity.is_integer():
                        quantity = int(quantity)
                except ValueError:
                    quantity = tokens[0]
                components.append({
                    'slug': tokens[2],
                    'quantity': quantity,
                    'unit': tokens[1]
                })
            elif len(tokens) == 2:
                components.append({
                    'quantity': tokens[0],
                    'slug': tokens[1],
                })
            else:
                components.append({
                    'slug': ' '.join(tokens)
                })

        return components

    @staticmethod
    def _get_origin(raw_recipe):
        if '?' in raw_recipe.citation_year:
            return {}
        else:
            return {
                'year': int(raw_recipe.citation_year)
            }

    @staticmethod
    def _get_glassware(instructions):

        for instruction in instructions:
            if 'glass' in instruction.get('text').lower():
                glass = re.sub(r"^(.*) (\w+) glass(.*)$", r'\2', instruction.get('text').lower())
                return [{'slug': Slug(glass)}]

    @staticmethod
    def _get_straw(instructions):

        for instruction in instructions:
            if 'straw' in instruction.get('text').lower():
                return True

        return False
