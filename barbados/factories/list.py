from barbados.factories.base import BaseFactory
from barbados.objects.list import List
from barbados.models.list import ListModel
from barbados.validators.listmodel import ListModelValidator
from barbados.indexes.list import ListIndex
from barbados.factories.parser import FactoryParser
from barbados.factories.listitem import ListItemFactory


class ListFactory(BaseFactory):
    _model = ListModel
    _validator = ListModelValidator
    _index = ListIndex

    required_keys = {
        'items': list(),
    }

    unwanted_keys = [
        'slug'  # This was deprecated
    ]

    @classmethod
    def raw_to_obj(cls, raw):
        raw_list = cls.sanitize_raw(raw, required_keys=cls.required_keys,
                                    unwanted_keys=cls.unwanted_keys)

        # Parse
        raw_list = FactoryParser.parse_id(raw_list)
        raw_list = FactoryParser.parse_display_name(raw_list, source_attr='id')
        raw_list = FactoryParser.parse_object_list(raw_list, factory=ListItemFactory, key='items')

        dl = List(**raw_list)
        return dl
