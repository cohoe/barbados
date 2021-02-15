from barbados.factories.base import BaseFactory
from barbados.factories.parser import FactoryParser
from barbados.objects.glassware import Glassware
from barbados.models.glassware import GlasswareModel
from barbados.validators.glasswaremodel import GlasswareModelValidator


class GlasswareFactory(BaseFactory):
    _model = GlasswareModel
    _validator = GlasswareModelValidator
    _index = None

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse fields
        raw_obj = FactoryParser.parse_display_name(raw_obj)

        return Glassware(**raw_obj)
