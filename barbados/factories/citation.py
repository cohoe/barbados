from barbados.objects.citation import Citation
from barbados.factories.base import BaseFactory
from barbados.factories.parser import FactoryParser


class CitationFactory(BaseFactory):

    required_keys = {
        'notes': list(),
        'date': None,
    }

    @classmethod
    def raw_to_obj(cls, raw):
        raw_c = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse the fields
        raw_c = FactoryParser.parse_text(raw_c, key='notes')
        raw_c = FactoryParser.parse_date(raw_c)

        return Citation(**raw_c)
