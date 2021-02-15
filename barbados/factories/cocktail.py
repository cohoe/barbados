import copy
from barbados.objects.cocktail import Cocktail
from barbados.objects.text import Slug
from barbados.factories.spec import SpecFactory
from barbados.factories.citation import CitationFactory
from barbados.serializers import ObjectSerializer
from barbados.factories.base import BaseFactory
from barbados.models.cocktail import CocktailModel
from barbados.validators.cocktailmodel import CocktailModelValidator
from barbados.indexes.recipe import RecipeIndex
from barbados.factories.text import TextFactory
from barbados.factories.parser import FactoryParser
from barbados.factories.origin import OriginFactory
from barbados.factories.image import ImageFactory
from barbados.caches.ingredienttree import IngredientTreeCache


class CocktailFactory(BaseFactory):
    _model = CocktailModel
    _validator = CocktailModelValidator
    _index = RecipeIndex

    required_keys = {
        'specs': list(),
        'citations': list(),
        'notes': list(),
        'tags': list(),
        'images': list(),
    }

    unwanted_keys = [
        'spec_count'
    ]

    @classmethod
    def raw_to_obj(cls, raw_c):
        raw_c = cls.sanitize_raw(raw_c, required_keys=cls.required_keys, unwanted_keys=cls.unwanted_keys)
        raw_c = FactoryParser.parse_display_name(raw_c)
        raw_c = FactoryParser.parse_object(raw_c, factory=OriginFactory, key='origin')
        raw_c = FactoryParser.parse_object_list(raw_c, factory=TextFactory, key='notes')
        raw_c = FactoryParser.parse_object_list(raw_c, factory=CitationFactory, key='citations')
        raw_c = FactoryParser.parse_object_list(raw_c, factory=ImageFactory, key='images')
        raw_c = FactoryParser.parse_object_list(raw_c, factory=SpecFactory, key='specs')

        return Cocktail(**raw_c)

    @classmethod
    def obj_to_index(cls, obj, format='dict'):
        base_recipe = ObjectSerializer.serialize(obj, format)
        base_recipe.update({'alpha': obj.alpha})

        tree = IngredientTreeCache.retrieve()

        specs = base_recipe.pop('specs')

        searchable_recipes = {}
        for spec in specs:
            # Holy Fuck this took too long to figure out
            # https://thispointer.com/python-how-to-copy-a-dictionary-shallow-copy-vs-deep-copy/
            searchable = copy.deepcopy(base_recipe)
            searchable['spec'] = spec
            searchable_id = '%s::%s' % (searchable['slug'], spec['slug'])
            searchable_recipes[searchable_id] = searchable

            # This count is achievable with a filter query in ES.
            # https://stackoverflow.com/questions/58659527/elastic-search-update-specific-nested-object
            # { filter: { script: { script: { source: "doc['spec.components.slug'].value.length() == 3" } } }
            # But it seemed to return some weird results too. Also required fielddata enabled on
            # the index. Also need to refactor the searchquer builder to deal with a deep parameter. This is
            # just easier.
            #
            # Maybe someday this will also bring back the notion of "countable" ingredients (ie, exclude bitters).
            # Given the complexity around that (requires parent to lookup, also ZK list of slugs to exclude)
            # it's not quite worth it right now.
            searchable['spec']['component_count'] = len(spec['components'])

            # https://stackoverflow.com/questions/14071038/add-an-element-in-each-dictionary-of-a-list-list-comprehension
            for component in spec['components']:
                # the Slug() is needed for the TDFv3 name->slug conversion.
                component.update({'parents': tree.parents(Slug(component['slug']))})

        return [cls._index(meta={'id': key}, **value) for key, value in searchable_recipes.items()]
