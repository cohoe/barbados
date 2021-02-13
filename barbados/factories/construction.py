from barbados.factories.base import BaseFactory
from barbados.models.construction import ConstructionModel
from barbados.objects.construction import Construction
from barbados.objects.text import DisplayName
from barbados.validators.constructionmodel import ConstructionModelValidator


class ConstructionFactory(BaseFactory):
    _model = ConstructionModel
    _validator = ConstructionModelValidator

    required_keys = {
        'default_instructions': list()
    }

    @classmethod
    def raw_to_obj(cls, raw):
        raw_c = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        raw_c = cls._parse_display_name(raw_c)

        return Construction(**raw_c)

    @staticmethod
    def _parse_display_name(raw_input):
        key = 'display_name'

        if raw_input.get(key) is None:
            raw_input.update({key: DisplayName(raw_input.get('slug'))})

        return raw_input
