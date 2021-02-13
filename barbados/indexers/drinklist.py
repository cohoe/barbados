from barbados.indexers.base import BaseIndexer
from barbados.factories.drinklistfactory import DrinkListFactory
from barbados.indexes import DrinkListIndex
from barbados.objects.drinklist import DrinkList


class DrinkListIndexer(BaseIndexer):

    for_class = DrinkList
    for_index = DrinkListIndex
    factory = DrinkListFactory
