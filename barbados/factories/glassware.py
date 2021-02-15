from barbados.factories.base import BaseFactory
from barbados.objects.glassware import Glassware


class GlasswareFactory(BaseFactory):

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)
        return Glassware(**raw_obj)
