from barbados.objects.citation import Citation
from barbados.objects.text import Text
from datetime import date as Date

class CitationFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_citation):
        raw_citation = CitationFactory.sanitize_raw(raw_citation)

        notes = []
        if 'notes' in raw_citation.keys():
            for note in raw_citation['notes']:
                notes.append(Text(text=note))
            del(raw_citation['notes'])

        if 'date' in raw_citation.keys():
            raw_date = raw_citation['date']
            del(raw_citation['date'])

            if type(raw_date) != Date:
                raise Exception("Date is invalid '%s'" % raw_date)
        else:
            raw_date = None

        c_obj = Citation(notes=notes, date=raw_date, **raw_citation)

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
