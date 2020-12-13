import json
from barbados.caches.base import CacheBase
from barbados.services.cache import Cache
from barbados.serializers import ObjectSerializer
from barbados.objects.bibliography import Bibliography
from barbados.caches import Caches


class RecipeBibliographyCache(CacheBase):
    """
    Cache a list of all Citations.
    """
    cache_key = 'recipe_bibliography_cache'

    @classmethod
    def populate(cls):
        serialized_citations = [ObjectSerializer.serialize(citation, 'dict') for citation in Bibliography().citations]
        Cache.set(cls.cache_key, json.dumps(serialized_citations))


Caches.register_cache(RecipeBibliographyCache)
