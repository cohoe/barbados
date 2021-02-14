from barbados.objects.speccomponent import SpecComponent
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
        raw_c = cls._parse_text(raw_c, key='notes')

        return SpecComponent(**raw_c)
