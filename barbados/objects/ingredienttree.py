from treelib import Node, Tree
from treelib.exceptions import NodeIDAbsentError
from barbados.models import IngredientModel
from barbados.objects.ingredientkinds import CategoryKind, FamilyKind
import logging


class IngredientTree:

    root_node = 'ingredients'

    def __init__(self, passes=5):
        self.tree = self._build_tree(passes=passes)

    def _build_tree(self, passes, root=root_node):
        tree = Tree()

        tree.create_node(root, root)
        for item in IngredientModel.get_by_kind(CategoryKind):
            tree.create_node(item.slug, item.slug, parent=root, data=self._create_tree_data(item))

        for item in IngredientModel.get_by_kind(FamilyKind):
            tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))

        ingredients_to_place = list(IngredientModel.get_usable_ingredients())
        for i in range(1, passes + 1):
            logging.debug("Pass %i/%i" % (i, passes))

            for item in ingredients_to_place[:]:
                if item.kind == FamilyKind.value:
                    ingredients_to_place.remove(item)
                    logging.debug("Skipping %s because it is a family." % item.slug)
                    continue
                try:
                    tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))
                    ingredients_to_place.remove(item)
                except NodeIDAbsentError:
                    logging.debug("skipping %s (Attempt %i/%s)" % (item.slug, i, passes))

            if len(ingredients_to_place) == 0:
                logging.info("All done after pass %i" % i)
                break

        return tree

    def subtree(self, node_id):
        try:
            return self.tree.subtree(node_id)
        except NodeIDAbsentError:
            raise KeyError("Node %s could not be found." % node_id)

    def parent(self, node_id):
        try:
            # bpointer was deprecated somewhere between 1.5.5 and 1.6.1, but they
            # broke is_root() which is used later on in this class. Freezing to
            # 1.5.5 to avoid dealing with this for the moment.
            parent_id = self.tree.get_node(node_id).bpointer
            return self.tree.get_node(parent_id)
        except AttributeError:
            raise KeyError("%s has no parent." % node_id)

    def node(self, node_id):
        node = self.tree.get_node(node_id)
        if not node:
            raise KeyError("Node %s could not be found." % node_id)

        return node

    def nodes(self):
        """
        Return a list of all nodes in the tree. The first node is the root
        node and doesn't conform to object properties, so we exclude it
        from the return.
        :return: List of treelib.Node's
        """
        return self.tree.all_nodes()[1:]

    def substitutions(self, node_id):
        """
        TODO:
        * masking certain ingredients
        * dont recommend categories or families
        * weighting? (favored: true)
        * limit results?
        :param node_id:
        :return:
        """
        node = self.node(node_id)
        parent = self.parent(node_id)
        parents = self.parents(node_id)

        children = node.fpointer
        siblings = parent.fpointer
        siblings.remove(node.identifier)
        elements = node.data['elements']

        return ({
            'self': node.identifier,
            'parent': parent.identifier,
            'parents': parents,
            'children': children + elements,
            'siblings': siblings,
        })

    def parents(self, node_id):
        parents = []

        node = self.node(node_id)
        while not node.is_root():
            parents.append(node.tag) if node.tag != node_id else None
            node = self.parent(node.tag)

        return parents

    @staticmethod
    def _create_tree_data(item):
        return ({
            'display_name': item.display_name,
            'kind': item.kind,
            'aliases': item.aliases,
            'elements': item.elements,
        })
