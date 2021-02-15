from barbados.factories.base import BaseFactory
from barbados.objects.text import Text


class TextFactory(BaseFactory):

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)
        return Text(**raw_obj)
