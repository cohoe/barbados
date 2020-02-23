from barbados.objects.ingredient import Ingredient


class IngredientFactory:
    def __init__(self):
        pass

    @staticmethod
    def to_obj(input_object):
        # @TODO make this more generic, other than just model.
        mapping = {
            'slug': input_object.slug,
            'display_name': input_object.display_name,
            'kind': input_object.kind,
            'parent': input_object.parent,
            'aliases': input_object.aliases,
            'elements': input_object.elements,
        }
        return Ingredient(**mapping)
