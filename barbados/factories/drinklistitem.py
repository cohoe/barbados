from barbados.factories.base import BaseFactory
from barbados.objects.drinklistitem import DrinkListItem


class DrinkListItemFactory(BaseFactory):

    @classmethod
    def raw_to_obj(cls, raw):
        raw_obj = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)
        return DrinkListItem(**raw_obj)
