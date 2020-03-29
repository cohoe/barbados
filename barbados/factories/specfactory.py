from barbados.objects.spec import Spec
from barbados.objects.origin import Origin
from barbados.objects.glassware import Glassware
from barbados.objects.speccomponent import SpecComponent
from barbados.objects.text import Text
from barbados.objects.garnish import Garnish
from barbados.objects.slug import Slug
from barbados.objects.displayname import DisplayName
from barbados.objects.construction import Construction
from .citationfactory import CitationFactory


class SpecFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_spec):
        if 'name' not in raw_spec.keys():
            raise Exception('Spec is missing name')

        raw_spec = SpecFactory.sanitize_raw(raw_spec)

        if raw_spec['origin'] is not None:
            origin_obj = Origin(**raw_spec['origin'])
        else:
            origin_obj = Origin()

        glassware_obj_list = []
        for glassware in raw_spec['glassware']:
            glassware_slug = Slug(glassware)
            glassware_display_name = DisplayName(glassware_slug)
            glassware_obj_list.append(Glassware(slug=glassware_slug, display_name=glassware_display_name))

        components = []
        # ingredients == specingredient == component. Yay evolution
        for raw_ingredient in raw_spec['ingredients']:
            component_slug = Slug(raw_ingredient['name'])
            component_display_name = DisplayName(component_slug)
            del (raw_ingredient['name'])
            spec_ing_obj = SpecComponent(slug=component_slug, display_name=component_display_name, **raw_ingredient)
            components.append(spec_ing_obj)
        # print(ingredient_obj_list)

        c_obj_list = CitationFactory.raw_list_to_obj(raw_spec['citations'])
        # print(c_obj_list)

        n_obj_list = []
        for note in raw_spec['notes']:
            n_obj_list.append(Text(text=note))
        # print(n_obj_list)

        straw = SpecFactory.infer_bool(raw_spec['straw'])
        # print(straw)

        garnish_obj_list = []
        for raw_garnish in raw_spec['garnish']:
            if type(raw_garnish) is dict:
                garnish_slug = Slug(raw_garnish['name'])
                garnish_quantity = raw_garnish['quantity']
                garnish_note = None
                if 'note' in raw_garnish.keys():
                    garnish_note = raw_garnish['note']
            else:
                garnish_slug = Slug(raw_garnish)
                garnish_quantity = None
                garnish_note = None

            garnish_obj_list.append(Garnish(slug=garnish_slug, quantity=garnish_quantity, note=garnish_note))
        # print(garnish_obj_list)

        instr_obj_list = []
        for instruction in raw_spec['instructions']:
            instr_obj_list.append(Text(text=instruction))
        # print(instr_obj_list)

        construction_obj = Construction(slug=raw_spec['construction'])

        s_obj = Spec(name=raw_spec['name'],
                     origin=origin_obj,
                     glassware=glassware_obj_list,
                     components=components,
                     citations=c_obj_list,
                     notes=n_obj_list,
                     straw=straw,
                     garnish=garnish_obj_list,
                     instructions=instr_obj_list,
                     construction=construction_obj,
                     )

        return s_obj

    @staticmethod
    def sanitize_raw(raw_spec):
        required_keys = {
            'name': None,
            'origin': None,
            'glassware': list(),
            'components': list(),
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

        lists = ['components', 'citations', 'notes', 'garnish', 'instructions', 'glassware']
        for key in lists:
            if raw_spec[key] is None:
                raw_spec[key] = required_keys[key]
            # As of Tortuga Data Format v2, glassware is a single string.
            # This is future-proofing for the ability to allow multiple
            # glassware definitions (likely to be defined as an | situation.
            if raw_spec[key].__class__ == str:
                raw_spec[key] = [raw_spec[key]]

        return raw_spec

    @staticmethod
    def infer_bool(input_value):
        """
        Infer a boolean from the given value
        :param input_value: String, Integer, Boolean, None
        :return: Boolean
        """
        # Boolean
        if isinstance(input_value, bool):
            return input_value

        # Integer
        if isinstance(input_value, int):
            return bool(input_value)

        # String
        if isinstance(input_value, str):
            if 'Y' in input_value.upper():
                return True
            else:
                return False

        # None
        if input_value is None:
            return False
