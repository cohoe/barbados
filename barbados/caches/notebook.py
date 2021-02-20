import json
from barbados.caches.base import CacheBase
from barbados.services.cache import CacheService
from barbados.serializers import ObjectSerializer
from barbados.objects.notebook import Notebook
from barbados.caches import Caches


class NotebookCache(CacheBase):
    """
    Cache a list of all notes.
    """
    cache_key = 'recipe_notebook_cache'

    @classmethod
    def populate(cls):
        serialized_notes = [ObjectSerializer.serialize(note, 'dict') for note in Notebook().notes]
        CacheService.set(cls.cache_key, json.dumps(serialized_notes))


Caches.register_cache(NotebookCache)
