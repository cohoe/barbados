from barbados.objects.cocktail import Cocktail, Status
from barbados.objects.origin import Origin
from barbados.text import Text
from .specfactory import SpecFactory
from .citationfactory import CitationFactory
from barbados.serializers import ObjectSerializer
from .base import BaseFactory
import copy
from barbados.caches import IngredientTreeCache


class CocktailFactory(BaseFactory):
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_recipe, slug):
        raw_recipe = CocktailFactory.sanitize_raw(raw_recipe)

        if raw_recipe.get('display_name') is None:
            raise Exception("display_name cannot be none")

        status_obj = Status(color=raw_recipe['status'])

        if raw_recipe['origin'] is not None:
            origin_obj = Origin(**raw_recipe['origin'])
        else:
            origin_obj = Origin()

        s_obj_list = []
        for raw_spec in raw_recipe['specs']:
            spec_obj = SpecFactory.raw_to_obj(raw_spec)
            s_obj_list.append(spec_obj)

        citation_obj_list = CitationFactory.raw_list_to_obj(raw_recipe['citations'])

        n_obj_list = []
        for note in raw_recipe['notes']:
            n_obj_list.append(Text(text=note))

        tag_obj_list = []
        for tag in raw_recipe['tags']:
            tag_obj_list.append(Text(text=tag))

        c_obj = Cocktail(display_name=raw_recipe['display_name'],
                         status=status_obj,
                         origin=origin_obj,
                         specs=s_obj_list,
                         citations=citation_obj_list,
                         notes=n_obj_list,
                         tags=tag_obj_list,
                         slug=slug)

        return c_obj

    @staticmethod
    def sanitize_raw(raw_recipe):
        required_keys = {
            'name': None,
            'status': None,
            'origin': None,
            'spec': list(),
            'citations': list(),
            'notes': list(),
            'tags': list(),
        }

        for key in required_keys.keys():
            if key not in raw_recipe.keys():
                raw_recipe[key] = required_keys[key]

        lists = ['spec', 'citations', 'notes', 'tags']
        for key in lists:
            if raw_recipe[key] is None:
                raw_recipe[key] = required_keys[key]

        return raw_recipe

    @staticmethod
    def model_to_obj(model):
        if model is None:
            raise KeyError('empty object')

        raw_data = {
            'display_name': model.display_name,
            'notes': model.notes,
            'specs': model.specs,
            'status': model.status,
        }

        return CocktailFactory.raw_to_obj(raw_recipe=raw_data, slug=model.slug)

    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        base_recipe = ObjectSerializer.serialize(obj, format)
        alpha = base_recipe['slug'][0]

        tree = IngredientTreeCache.retrieve()
        try:
            alpha = int(alpha)
            base_recipe['alpha'] = '#'
        except ValueError:
            base_recipe['alpha'] = alpha
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
                component.update({'parents': tree.parents(component['slug'])})

        return [index_class(meta={'id': key}, **value) for key, value in searchable_recipes.items()]
