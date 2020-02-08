from barbados.objects import Ingredient


class IngredientFactory:
    def __init__(self):
        pass

    @staticmethod
    def node_to_obj(node):
        return Ingredient(slug=node.tag, display_name=node.data['display_name'], type=node.data['type'], parent=node.bpointer)