from barbados.objects import Citation


class CitationFactory:
    def __init__(self):
        pass

    @staticmethod
    def raw_to_obj(raw_citation):
        raw_citation = CitationFactory.sanitize_raw(raw_citation)
        c_obj = Citation(**raw_citation)

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
