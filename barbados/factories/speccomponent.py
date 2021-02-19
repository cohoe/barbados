from barbados.objects.speccomponent import SpecComponent
from barbados.factories.base import BaseFactory
from barbados.factories.parser import FactoryParser
from barbados.factories.text import TextFactory
from barbados.factories.ingredient import IngredientFactory


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
        raw_c = FactoryParser.parse_slug(raw_c)
        raw_c = FactoryParser.parse_object_list(raw_c, factory=TextFactory, key='notes')
        raw_c = FactoryParser.parse_preparation(raw_c)

        # Fill in any blanks from the source of truth.
        i = IngredientFactory.produce_obj(id=raw_c.get('slug'))
        raw_c = FactoryParser.parse_display_name(raw_c, custom_fallback_value=i.display_name)

        return SpecComponent(**raw_c)
