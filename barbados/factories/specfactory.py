from barbados.objects.spec import Spec
from barbados.objects.origin import Origin
from barbados.glassware import Glassware
from barbados.objects.speccomponent import SpecComponent
from barbados.text import Text, Slug, DisplayName
from barbados.objects.construction import Construction
from .citationfactory import CitationFactory
from barbados.objects.image import Image


class SpecFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_spec):
        # Tortuga Data Format v3 replaced all names with slugs, but it means that
        # the slugs for specs are not accurate. Same problem for ingredients.
        spec_slug = Slug(raw_spec['slug'])
        try:
            spec_display_name = raw_spec['display_name']
        except KeyError:
            spec_display_name = DisplayName(spec_slug)

        raw_spec = SpecFactory.sanitize_raw(raw_spec)

        if raw_spec['origin'] is not None:
            origin_obj = Origin(**raw_spec['origin'])
        else:
            origin_obj = Origin()

        glassware_obj_list = []
        for glassware in raw_spec['glassware']:
            if type(glassware) is dict:
                glassware_obj_list.append(Glassware(**glassware))
            else:
                glassware_slug = Slug(glassware)
                glassware_display_name = DisplayName(glassware_slug)
                glassware_obj_list.append(Glassware(slug=glassware_slug, display_name=glassware_display_name))

        components = []
        # ingredients == specingredient == component. Yay evolution
        for raw_ingredient in raw_spec['components']:
            try:
                component_slug = Slug(raw_ingredient['name'])
                component_display_name = DisplayName(component_slug)
                del (raw_ingredient['name'])

                notes = []
                if 'notes' in raw_ingredient.keys():
                    notes = [Text(**note) for note in raw_ingredient['notes']]
                    del (raw_ingredient['notes'])
                spec_ing_obj = SpecComponent(slug=component_slug, display_name=component_display_name, notes=notes, **raw_ingredient)
            except KeyError:
                notes = []
                if 'notes' in raw_ingredient.keys():
                    notes = [Text(**note) for note in raw_ingredient['notes']]
                    raw_ingredient.update({'notes': notes})
                raw_ingredient.update({'slug': Slug(raw_ingredient.get('slug'))})
                spec_ing_obj = SpecComponent(**raw_ingredient)

            components.append(spec_ing_obj)
        # print(ingredient_obj_list)

        c_obj_list = CitationFactory.raw_list_to_obj(raw_spec['citations'])
        # print(c_obj_list)

        n_obj_list = []
        for note in raw_spec['notes']:
            if type(note) is dict:
                n_obj_list.append(Text(**note))
            else:
                n_obj_list.append(Text(text=note))
        # print(n_obj_list)

        straw = SpecFactory.infer_bool(raw_spec['straw'])
        # print(straw)

        garnish_obj_list = []
        for raw_garnish in raw_spec['garnish']:
            if 'notes' in raw_garnish.keys():
                notes = []
                for raw_note in raw_garnish.get('notes'):
                    notes.append(Text(**raw_note))
                raw_garnish['notes'] = notes

            garnish_obj = SpecComponent(**raw_garnish)

            garnish_obj_list.append(garnish_obj)
        # print(garnish_obj_list)

        instr_obj_list = []
        for instruction in raw_spec['instructions']:
            if type(instruction) is dict:
                instr_obj_list.append(Text(**instruction))
            else:
                instr_obj_list.append(Text(text=instruction))
        # print(instr_obj_list)

        if type(raw_spec['construction']) is dict:
            construction_obj = Construction(**raw_spec['construction'])
        else:
            construction_obj = Construction(slug=raw_spec['construction'])

        image_obj_list = []
        for image in raw_spec['images']:
            image_obj_list.append(Image(**image))

        s_obj = Spec(slug=spec_slug,
                     display_name=spec_display_name,
                     origin=origin_obj,
                     glassware=glassware_obj_list,
                     components=components,
                     citations=c_obj_list,
                     notes=n_obj_list,
                     straw=straw,
                     garnish=garnish_obj_list,
                     instructions=instr_obj_list,
                     construction=construction_obj,
                     images=image_obj_list,
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
            'images': list(),
        }

        for key in required_keys.keys():
            if key not in raw_spec.keys():
                raw_spec[key] = required_keys[key]

        lists = ['components', 'citations', 'notes', 'garnish', 'instructions', 'glassware', 'images']
        for key in lists:
            if raw_spec[key] is None:
                raw_spec[key] = required_keys[key]

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
