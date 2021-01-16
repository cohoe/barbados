from barbados.factories.base import BaseFactory
from barbados.objects.text import DisplayName
from barbados.objects.menu import Menu
from barbados.objects.menuitem import MenuItem
from barbados.models.menu import MenuModel


class MenuFactory(BaseFactory):
    _model = MenuModel

    @staticmethod
    def model_to_obj(model):
        if model is None:
            raise KeyError('empty object')

        return MenuFactory.raw_to_obj(model.__dict__)

    @staticmethod
    def raw_to_obj(raw):
        raw_menu = MenuFactory.sanitize_raw(raw)

        if not raw_menu.get('display_name'):
            raw_menu.update({'display_name', DisplayName(raw_menu.get('slug'))})

        menu_item_list = []
        for raw_item in raw_menu.get('items'):
            mi = MenuItem(**raw_item)
            menu_item_list.append(mi)

        m = Menu(slug=raw_menu.get('slug'), display_name=raw_menu.get('display_name'),
                 items=menu_item_list)

        return m

    @staticmethod
    def sanitize_raw(raw_input):
        required_keys = {
            'slug': None,
            'display_name': None,
            'items': list(),
        }

        for key in required_keys.keys():
            # If the required key is not in the input, set it to the default above.
            if key not in raw_input.keys():
                raw_input[key] = required_keys[key]
            # If the required key should be a list and in the input it is not, force
            # it to an empty list.
            if type(required_keys[key]) is list:
                if raw_input[key] is None:
                    raw_input[key] = required_keys[key]

        return raw_input
