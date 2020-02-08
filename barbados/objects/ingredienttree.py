from treelib import Node, Tree
from treelib.exceptions import NodeIDAbsentError
from barbados.models import IngredientModel
from barbados.constants import IngredientTypes


class IngredientTree:
    def __init__(self, root='ingredients', passes=5):
        self.tree = self._build_tree(root=root, passes=passes)

    def _build_tree(self, root, passes):
        tree = Tree()

        tree.create_node(root, root)
        for item in IngredientModel.get_by_type(IngredientTypes.CATEGORY):
            tree.create_node(item.slug, item.slug, parent=root, data=self._create_tree_data(item))

        for item in IngredientModel.get_by_type(IngredientTypes.FAMILY):
            tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))

        ingredients_to_place = list(IngredientModel.get_by_type(IngredientTypes.INGREDIENT))

        for i in range(1, passes+1):
            print("Pass %i/%i" % (i, passes))

            for item in ingredients_to_place[:]:
                try:
                    tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))
                    ingredients_to_place.remove(item)
                except NodeIDAbsentError:
                    print("skipping %s (Attempt %i/%s)" % (item.slug, i, passes))

            if len(ingredients_to_place) == 0:
                print("All done after pass %i" % i)
                break

        return tree

    def subtree(self, node_id):
        return self.tree.subtree(node_id)

    def parent(self, node_id):
        parent_id = self.tree.get_node(node_id).bpointer
        return self.tree.get_node(parent_id)

    def node(self, node_id):
        node = self.tree.get_node(node_id)
        if not node:
            raise KeyError("Node %s could not be found." % node_id)

        return node

    @staticmethod
    def _create_tree_data(item):
        return ({
            'display_name': item.display_name,
            'type': item.type,
        })
