from barbados.objects.cocktail import Cocktail, Status
from barbados.objects.origin import Origin
from barbados.objects.text import Text
from .specfactory import SpecFactory
from .citationfactory import CitationFactory
from barbados.serializers import ObjectSerializer


class CocktailFactory:
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
    def obj_to_index(obj, index_class):
        return index_class(meta={'id': obj.slug}, **ObjectSerializer.serialize(obj, 'dict'))