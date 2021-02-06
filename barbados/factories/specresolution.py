from barbados.factories.base import BaseFactory
from barbados.serializers import ObjectSerializer
from barbados.objects.resolution.summary import SpecResolutionSummary
from uuid import uuid4, UUID
from barbados.objects.resolution import Resolution
from barbados.objects.speccomponent import SpecComponent
from barbados.objects.text import Text
from barbados.factories.citationfactory import CitationFactory


class SpecResolutionFactory(BaseFactory):
    _model = None
    required_keys = {
        'alpha': str(),
        'citations': list(),
        'cocktail_slug': str(),
        'component_count': int(),
        'components': list(),
        'construction_slug': str(),
        'garnish': list(),
        'inventory_id': uuid4(),
        'spec_slug': str(),
        'status_count': dict(),
        # 'notes': list(),
    }

    @classmethod
    def model_to_obj(cls, model):
        """
        There is no Model with which to parse.
        :param model:
        :return:
        """
        pass

    @classmethod
    def raw_to_obj(cls, raw):
        raw_srs = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys)

        # Parse the fields
        raw_srs = cls._parse_inventory_id(raw_srs)
        raw_srs = cls._parse_components(raw_srs)
        raw_srs = cls._parse_garnish(raw_srs)
        raw_srs = cls._parse_citations(raw_srs)
        # raw_srs = cls._parse_notes(raw_srs)

        return SpecResolutionSummary(**raw_srs)

    @staticmethod
    def _parse_inventory_id(raw_input):
        key = 'inventory_id'

        raw_id = raw_input.get(key)
        raw_input.update({key: UUID(raw_id)})

        return raw_input

    @staticmethod
    def _parse_components(raw_input):
        key = 'components'

        objs = []
        for raw_component in raw_input.get(key):
            r = Resolution(**raw_component)
            objs.append(r)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_garnish(raw_input):
        key = 'garnish'

        objs = []
        for raw_garnish in raw_input.get(key):
            # @TODO techically this means factory
            if raw_garnish.get('notes'):
                notes = []
                [notes.append(Text(**n)) for n in raw_garnish.get('notes')]
                raw_garnish.update({'notes': notes})
            s = SpecComponent(**raw_garnish)
            objs.append(s)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_citations(raw_input):
        key = 'citations'

        objs = []
        for raw_citation in raw_input.get(key):
            c = CitationFactory.raw_to_obj(raw_citation)
            objs.append(c)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_notes(raw_input):
        key = 'notes'

        objs = []
        for raw_note in raw_input.get(key):
            n = Text(**raw_note)
            objs.append(n)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        """
        Serialize an object into a standard form suitable
        for indexing.
        :param obj: Serializable object.
        :param index_class: The ElasticSearch DSL class representing the intended index.
        :param format: Format of the data to pass to the serializer.
        :return: Instance of the Index class.
        """
        return index_class(meta={'id': obj.index_id}, **ObjectSerializer.serialize(obj, format))

    @classmethod
    def index_to_obj(cls, indexable):
        raw_indexable = indexable.to_dict()
        return cls.raw_to_obj(raw_indexable)

    @classmethod
    def from_objects(cls, inventory, cocktail, spec):
        return SpecResolutionSummary(inventory_id=inventory.id, cocktail_slug=cocktail.slug, spec_slug=spec.slug,
                                     alpha=cocktail.alpha, citations=spec.citations + cocktail.citations,
                                     components=[], construction_slug=spec.construction.slug, garnish=spec.garnish)
