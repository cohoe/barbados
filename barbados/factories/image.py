from barbados.factories.base import BaseFactory
from barbados.objects.image import Image


class ImageFactory(BaseFactory):

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)
        return Image(**raw_obj)
