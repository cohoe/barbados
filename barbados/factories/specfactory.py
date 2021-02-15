from barbados.factories.base import BaseFactory
from barbados.objects.spec import Spec
from barbados.factories.citation import CitationFactory
from barbados.factories.construction import ConstructionFactory
from barbados.factories.text import TextFactory
from barbados.factories.speccomponent import SpecComponentFactory
from barbados.factories.image import ImageFactory
from barbados.factories.glassware import GlasswareFactory
from barbados.factories.origin import OriginFactory
from barbados.factories.parser import FactoryParser


class SpecFactory(BaseFactory):

    required_keys = {
        'origin': None,
        'glassware': list(),
        'components': list(),
        'citations': list(),
        'notes': list(),
        'straw': None,
        'garnish': list(),
        'instructions': list(),
        'construction': None,
        'images': list(),
    }

    @classmethod
    def raw_to_obj(cls, raw_spec):
        raw_spec = cls.sanitize_raw(raw_input=raw_spec, required_keys=cls.required_keys)
        raw_spec = FactoryParser.parse_slug(raw_spec)
        raw_spec = FactoryParser.parse_display_name(raw_spec)
        raw_spec = FactoryParser.parse_object(raw_spec, factory=OriginFactory, key='origin')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=GlasswareFactory, key='glassware')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=SpecComponentFactory, key='components')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=CitationFactory, key='citations')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=TextFactory, key='notes')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=TextFactory, key='instructions')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=SpecComponentFactory, key='garnish')
        raw_spec = FactoryParser.parse_object_list(raw_spec, factory=ImageFactory, key='images')
        raw_spec = FactoryParser.parse_object(raw_spec, factory=ConstructionFactory, key='construction')
        raw_spec = FactoryParser.parse_boolean(raw_spec, key='straw')

        return Spec(**raw_spec)
