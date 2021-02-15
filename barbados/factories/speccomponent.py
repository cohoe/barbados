from barbados.objects.speccomponent import SpecComponent
from barbados.factories.base import BaseFactory
from barbados.factories.parser import FactoryParser
from barbados.factories.text import TextFactory


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
        raw_c = FactoryParser.parse_object_list(raw_c, factory=TextFactory, key='notes')

        return SpecComponent(**raw_c)
