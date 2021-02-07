from barbados.objects.speccomponent import SpecComponent
from barbados.objects.text import Text
from barbados.factories.base import BaseFactory


class SpecComponentFactory(BaseFactory):
    _model = None
    _validator = None

    required_keys = {
        'notes': list(),
    }

    @classmethod
    def raw_to_obj(cls, raw):
        raw_c = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse the fields
        raw_c = cls._parse_notes(raw_c)

        return SpecComponent(**raw_c)

    @staticmethod
    def _parse_notes(raw_input):
        key = 'notes'

        objs = []
        for note in raw_input['notes']:
            objs.append(Text(**note))
        raw_input.update({key: objs})

        return raw_input
