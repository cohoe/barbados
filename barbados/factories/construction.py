from barbados.factories.base import BaseFactory
from barbados.models.construction import ConstructionModel
from barbados.objects.construction import Construction
from barbados.validators.constructionmodel import ConstructionModelValidator
from barbados.factories.parser import FactoryParser


class ConstructionFactory(BaseFactory):
    _model = ConstructionModel
    _validator = ConstructionModelValidator
    _index = None

    required_keys = {
        'default_instructions': list()
    }

    @classmethod
    def raw_to_obj(cls, raw):
        raw_c = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        raw_c = FactoryParser.parse_display_name(raw_c)

        return Construction(**raw_c)
