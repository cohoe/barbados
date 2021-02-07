from barbados.objects.citation import Citation
from barbados.objects.text import Text
from datetime import date as Date
from barbados.factories.base import BaseFactory


class CitationFactory(BaseFactory):
    _model = None
    _validator = None

    required_keys = {
        'notes': list(),
        'date': None,
    }

    @classmethod
    def raw_to_obj(cls, raw):
        raw_c = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse the fields
        raw_c = cls._parse_notes(raw_c)
        raw_c = cls._parse_date(raw_c)

        return Citation(**raw_c)

    @staticmethod
    def _parse_notes(raw_input):
        # @TODO this should be a factory
        key = 'notes'

        objs = []
        for note in raw_input['notes']:
            objs.append(Text(**note))
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_date(raw_input):
        key = 'date'

        # raw_date is not a Date() when it comes from YAML but
        # is a Str() when it comes from database or other sources.
        # There is a way of disabling the auto-casting in the yaml
        # loader, it may be a good idea to revisit that.
        raw_date = raw_input.get(key)

        if type(raw_date) is Date:
            new_date = raw_date.year
        elif type(raw_date) is str:
            new_date = Date(*[int(i) for i in raw_date.split('-')]).year
        elif type(raw_date) is int:
            new_date = raw_date
        else:
            new_date = None

        raw_input.update({key: new_date})
        return raw_input
