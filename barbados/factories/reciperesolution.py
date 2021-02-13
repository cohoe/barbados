from barbados.factories.base import BaseFactory
from barbados.serializers import ObjectSerializer
from barbados.objects.resolution.summary import RecipeResolutionSummary
from uuid import uuid4, UUID
from barbados.objects.resolution.speccomponent import SpecComponentResolution
from barbados.objects.text import Text
from barbados.factories.citation import CitationFactory
from barbados.factories.speccomponent import SpecComponentFactory
from barbados.models.reciperesolutionsummary import RecipeResolutionSummaryModel
from barbados.services.database import DatabaseService
from barbados.indexes.reciperesolutionindex import RecipeResolutionIndex


class RecipeResolutionFactory(BaseFactory):
    _model = RecipeResolutionSummaryModel
    _validator = None
    _index = RecipeResolutionIndex

    required_keys = {
        'alpha': str(),
        'citations': list(),
        'cocktail_slug': str(),
        'components': list(),
        'construction_slug': str(),
        'garnish': list(),
        'inventory_id': uuid4(),
        'spec_slug': str(),
        'status_count': dict(),
    }

    unwanted_keys = [
        'component_count',
        'id',
        'status_count'
    ]

    @classmethod
    def raw_to_obj(cls, raw):
        raw_srs = cls.sanitize_raw(raw_input=raw, required_keys=cls.required_keys, unwanted_keys=cls.unwanted_keys)

        # Parse the fields
        raw_srs = cls._parse_inventory_id(raw_srs)
        raw_srs = cls._parse_components(raw_srs)
        raw_srs = cls._parse_garnish(raw_srs)
        raw_srs = cls._parse_citations(raw_srs)

        return RecipeResolutionSummary(**raw_srs)

    @staticmethod
    def _parse_inventory_id(raw_input):
        key = 'inventory_id'

        if type(raw_input.get(key)) is not UUID:
            raw_id = raw_input.get(key)
            raw_input.update({key: UUID(raw_id)})

        return raw_input

    @staticmethod
    def _parse_components(raw_input):
        key = 'components'

        objs = []
        for raw_component in raw_input.get(key):
            r = SpecComponentResolution(**raw_component)
            objs.append(r)
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_garnish(raw_input):
        key = 'garnish'

        objs = SpecComponentFactory.raw_list_to_obj(raw_input.get(key))
        raw_input.update({key: objs})

        return raw_input

    @staticmethod
    def _parse_citations(raw_input):
        key = 'citations'

        objs = CitationFactory.raw_list_to_obj(raw_input.get(key))
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

    @classmethod
    def obj_to_index(cls, obj, format='dict'):
        """
        Serialize an object into a standard form suitable
        for indexing.
        :param obj: Serializable object.
        :param format: Format of the data to pass to the serializer.
        :return: Instance of the Index class.
        """
        return cls._index(meta={'id': obj.id}, **ObjectSerializer.serialize(obj, format))

    @classmethod
    def index_to_obj(cls, indexable):
        raw_indexable = indexable.to_dict()
        return cls.raw_to_obj(raw_indexable)

    @classmethod
    def obj_to_model(cls, obj):
        raw_dict = ObjectSerializer.serialize(obj, 'dict')
        raw_dict.update({'id': obj.id})
        return cls._model(**raw_dict)

    @classmethod
    def from_objects(cls, inventory, cocktail, spec):
        return RecipeResolutionSummary(inventory_id=inventory.id, cocktail_slug=cocktail.slug, spec_slug=spec.slug,
                                       alpha=cocktail.alpha, citations=spec.citations + cocktail.citations,
                                       components=[], construction_slug=spec.construction.slug, garnish=spec.garnish)

    @classmethod
    def produce_all_objs_from_inventory(cls, inventory_id):
        """
        :return:
        """
        with DatabaseService.get_session() as session:
            results = session.query(RecipeResolutionSummaryModel).filter(RecipeResolutionSummaryModel.inventory_id==inventory_id)

            objects = []
            for result in results:
                obj = cls.model_to_obj(result)
                objects.append(obj)

        return objects
