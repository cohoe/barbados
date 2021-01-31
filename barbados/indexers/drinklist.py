from barbados.indexers.base import BaseIndexer
from barbados.factories.drinklistfactory import DrinkListFactory
from barbados.indexes import DrinkListIndex
from barbados.objects.drinklist import DrinkList


class DrinkListIndexer(BaseIndexer):

    for_class = DrinkList
    for_index = DrinkListIndex
    factory = DrinkListFactory

    @staticmethod
    def index(dl_object):
        index = DrinkListFactory.obj_to_index(dl_object, DrinkListIndex)
        index.save()

    # @TODO make generic?
    @staticmethod
    def delete(dl_object):
        index = DrinkListFactory.obj_to_index(dl_object, DrinkListIndex)
        DrinkListIndex.delete(index)
