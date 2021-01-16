import copy
from treelib import Node, Tree
from treelib.exceptions import NodeIDAbsentError
from barbados.models.ingredient import IngredientModel
from barbados.objects.ingredientkinds import IngredientKinds, CategoryKind, FamilyKind
from barbados.services.logging import LogService
from barbados.services.registry import RegistryService


class IngredientTree:
    root_node = 'ingredients'

    def __init__(self, passes=5):
        self.tree = self._build_tree(passes=passes)

    def _build_tree(self, passes, root=root_node):
        tree = Tree()

        pgconn = RegistryService.get_database_connection()
        with pgconn.get_session() as session:

            tree.create_node(root, root)
            for item in IngredientModel.get_by_kind(session, CategoryKind):
                tree.create_node(item.slug, item.slug, parent=root, data=self._create_tree_data(item))

            for item in IngredientModel.get_by_kind(session, FamilyKind):
                tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))

            ingredients_to_place = list(IngredientModel.get_usable_ingredients(session))
            for i in range(1, passes + 1):
                LogService.debug("Pass %i/%i" % (i, passes))

                for item in ingredients_to_place[:]:
                    if item.kind == FamilyKind.value:
                        ingredients_to_place.remove(item)
                        LogService.debug("Skipping %s because it is a family." % item.slug)
                        continue
                    try:
                        tree.create_node(item.slug, item.slug, parent=item.parent, data=self._create_tree_data(item))
                        ingredients_to_place.remove(item)
                    except NodeIDAbsentError:
                        LogService.debug("skipping %s (Attempt %i/%s)" % (item.slug, i, passes))

                if len(ingredients_to_place) == 0:
                    LogService.info("All done after pass %i" % i)
                    break

        return tree

    def subtree(self, node_id):
        try:
            return self.tree.subtree(node_id)
        except NodeIDAbsentError:
            raise KeyError("Node %s could not be found." % node_id)

    def parent(self, node_id):
        """
        @TODO this should return a string like the rest of my functions.
        :param node_id:
        :return:
        """
        try:
            # bpointer was deprecated somewhere between 1.5.5 and 1.6.1, but they
            # broke is_root() which is used later on in this class. Freezing to
            # 1.5.5 to avoid dealing with this for the moment.
            parent_id = self.tree.get_node(node_id).bpointer
            return self.tree.get_node(parent_id)
        except AttributeError:
            raise KeyError("%s has no parent." % node_id)

    def node(self, node_id):
        """
        Get a single node from the tree by tag (id, aka slug).
        :param node_id: ID to get.
        :return: The node object.
        """
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
        siblings = self.siblings(node_id)

        children = node.fpointer

        return ({
            'self': node.identifier,
            'parent': parent.identifier,
            'parents': parents,
            'children': children + node.data.get('elements'),
            'siblings': siblings,
            'kind': node.data.get('kind')
        })

    def siblings(self, node_id):
        """
        Return a list of all sibling nodes of this node. Siblings share the
        same parent. Note that siblings does NOT include children of this
        node.
        :param node_id: ID of the node to investigate.
        :return: List of node tags.
        """
        node = self.node(node_id)
        parent = self.parent(node_id)

        # I don't know how long this bug was there, but my gods...
        # Apparently I was deleting a bunch of stuff from the tree!
        # Remove this node from the list of siblings.
        siblings = copy.deepcopy(parent.fpointer)
        siblings.remove(node.identifier)

        return siblings

    def parents(self, node_id):
        """
        Return a list of all parent nodes of this node going up to the root.
        :param node_id: ID of the node to investigate.
        :return: List of node tags.
        """
        parents = []

        node = self.node(node_id)
        while not node.is_root():
            parents.append(node.tag) if node.tag != node_id else None
            node = self.parent(node.tag)

        return parents

    def children(self, node_id, extended=False):
        """
        Return a list of all children nodes of this node.
        :param node_id: ID of the node to investigate.
        :param extended: Include more than just the direct descendants of this
                         node (ie, all levels following.)
        :return: List of node tags.
        """
        if extended:
            # Subtree returns all nodes including this one.
            # We need to remove ourselves so we're not our own
            # child and then grab the Node() objects from the hash
            # that the subtree call gave us. Also because Python3
            # we have to turn the dict_values() object into a list
            # so that other things don't barf.
            subtree = self.subtree(node_id).nodes
            subtree.pop(node_id, None)
            children = [node.tag for node in list(subtree.values())]
        else:
            # Single-generation children are much easier to deal with.
            # #GeneologyGeoke
            children = [node.tag for node in self.tree.children(node_id)]

        return children

    @staticmethod
    def _create_tree_data(item):
        return ({
            'display_name': item.display_name,
            'kind': item.kind,
            'aliases': item.aliases,
            'elements': item.elements,
        })

    def implies(self, node_id):
        """
        Return a list of all ingredients that this node implies.
        This is done by looking at all parent ingredients up
        to the family, children, and siblings.
        Examples:
          * the-dead-rabbit-irish-whiskey -> [irish-whiskey, jameson-irish-whiskey]
          * el-dorado-12-year-rum -> [aged-blended-rum, aged-rum, rum]
          * orange-bitters -> [citrus-bitters, angostura-orange-bitters, regans-orange-bitters, grapefruit-bitters]
        :param node_id: ID of the node to investigate.
        :return: List of node tags (slugs).
        """
        implied_nodes = self.parents(node_id) + self.children(node_id, extended=True) + self.siblings(node_id)
        # print(node_id) if 'gin' in node_id else None
        # print(implied_nodes) if 'gin' in node_id else None
        # Log.info("All parents of %s are: %s" % (node_id, parents))

        # Figure out which IngredientKinds we allow for implicit substitution.
        implicit_kind_values = [kind.value for kind in IngredientKinds.implicits]
        # Log.info("Allowed implicit kinds are: %s" % implicit_kind_values)

        # Create a list of allowed parents based on whether the parent is
        # of an approved type.
        allowed_implicit_nodes = []
        for implied_node_id in implied_nodes:
            implied_node = self.node(node_id=implied_node_id)
            implied_node_kind = implied_node.data.get('kind')
            # Log.info("Kind of parent %s is %s" % (parent, parent_kind))

            if implied_node_kind in implicit_kind_values:
                allowed_implicit_nodes.append(implied_node_id)

        # Log.info("Allowed implicit nodes for %s are: %s" % (node_id, allowed_implicit_nodes))
        return allowed_implicit_nodes
