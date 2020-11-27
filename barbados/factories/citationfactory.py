from barbados.objects.citation import Citation
from barbados.text import Text
from datetime import date as Date
from barbados.exceptions import ValidationException


class CitationFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_citation):
        raw_citation = CitationFactory.sanitize_raw(raw_citation)

        notes = []
        if 'notes' in raw_citation.keys():
            for note in raw_citation['notes']:
                notes.append(Text(**note))
            del(raw_citation['notes'])

        # Frak the specific date, just go with year. Not all books make the
        # full publishing date easily available.
        if 'date' in raw_citation.keys():
            raw_date = raw_citation['date']
            del(raw_citation['date'])

            # raw_date is not a Date() when it comes from YAML but
            # is a Str() when it comes from database or other sources.
            # There is a way of disabling the auto-casting in the yaml
            # loader, it may be a good idea to revisit that.

            if type(raw_date) is Date:
                new_date = raw_date.year
            elif type(raw_date) is str:
                new_date = Date(*[int(i) for i in raw_date.split('-')]).year
            elif type(raw_date) is int:
                new_date = raw_date
            else:
                raise ValidationException("Date is invalid '%s'" % raw_date)
        else:
            new_date = None

        # Build and return the Citation object
        c_obj = Citation(notes=notes, date=new_date, **raw_citation)
        return c_obj

    @staticmethod
    def raw_list_to_obj(raw_citations):
        if not isinstance(raw_citations, list):
            raise Exception("Calling raw_list_to_obj on a not-list?")

        c_objs = []
        for raw_citation in raw_citations:
            c = CitationFactory.raw_to_obj(raw_citation)
            c_objs.append(c)

        return c_objs

    @staticmethod
    def sanitize_raw(raw_citation):
        return raw_citation
