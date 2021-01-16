from barbados.indexers.base import BaseIndexer
from barbados.factories import MenuFactory
from barbados.indexes import MenuIndex
from barbados.objects.menu import Menu


class MenuIndexer(BaseIndexer):

    for_class = Menu
    for_index = MenuIndex
    factory = MenuFactory

    @staticmethod
    def index(menu_object):
        index = MenuFactory.obj_to_index(menu_object, MenuIndex)
        index.save()

    # @TODO make generic?
    @staticmethod
    def delete(menu_object):
        index = MenuFactory.obj_to_index(menu_object, MenuIndex)
        MenuIndex.delete(index)
