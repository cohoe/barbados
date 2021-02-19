from barbados.indexers.base import BaseIndexer
from barbados.factories.list import ListFactory
from barbados.indexes import ListIndex
from barbados.objects.list import List


class ListIndexer(BaseIndexer):

    for_class = List
    for_index = ListIndex
    factory = ListFactory
