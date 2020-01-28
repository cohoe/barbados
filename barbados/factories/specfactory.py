import barbados.util
from barbados.objects import Spec, Origin, Glassware, SpecIngredient, Text
from .citationfactory import CitationFactory


class SpecFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_spec):
        if 'name' not in raw_spec.keys():
            barbados.util.die('Spec is missing name')

        raw_spec = SpecFactory.sanitize_raw(raw_spec)

        if raw_spec['origin'] is not None:
            origin_obj = Origin(**raw_spec['origin'])
        else:
            origin_obj = Origin()

        glassware_obj = Glassware(name=raw_spec['glassware'])

        ingredient_obj_list = []
        for raw_ingredient in raw_spec['ingredients']:
            spec_ing_obj = SpecIngredient(**raw_ingredient)
            ingredient_obj_list.append(spec_ing_obj)
        # print(ingredient_obj_list)

        c_obj_list = CitationFactory.raw_list_to_obj(raw_spec['citations'])
        # print(c_obj_list)

        n_obj_list = []
        for note in raw_spec['notes']:
            n_obj_list.append(Text(text=note))
        # print(n_obj_list)

        straw = barbados.util.infer_bool(raw_spec['straw'])
        # print(straw)

        garnish_obj_list = []
        for raw_garnish in raw_spec['garnish']:
            garnish_obj_list.append(SpecIngredient(name=raw_garnish))
        # print(garnish_obj_list)

        instr_obj_list = []
        for instruction in raw_spec['instructions']:
            instr_obj_list.append(Text(text=instruction))
        # print(instr_obj_list)

        # @TODO enum for construction

        s_obj = Spec(name=raw_spec['name'],
                     origin=origin_obj,
                     glassware=glassware_obj,
                     ingredients=ingredient_obj_list,
                     citations=c_obj_list,
                     notes=n_obj_list,
                     straw=straw,
                     garnish=garnish_obj_list,
                     instructions=instr_obj_list,
                     construction=raw_spec['construction'])

        return s_obj

    @staticmethod
    def sanitize_raw(raw_spec):
        required_keys = {
            'name': None,
            'origin': None,
            'glassware': None,
            'ingredients': list(),
            'citations': list(),
            'notes': list(),
            'straw': None,
            'garnish': list(),
            'instructions': list(),
            'construction': None,
        }

        for key in required_keys.keys():
            if key not in raw_spec.keys():
                raw_spec[key] = required_keys[key]

        lists = ['ingredients', 'citations', 'notes', 'garnish', 'instructions']
        for key in lists:
            if raw_spec[key] is None:
                raw_spec[key] = required_keys[key]

        return raw_spec
