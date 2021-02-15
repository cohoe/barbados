from barbados.factories.base import BaseFactory
from barbados.objects.origin import Origin


class OriginFactory(BaseFactory):

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)
        return Origin(**raw_obj) if raw_obj else Origin()
