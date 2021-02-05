from barbados.resolvers.base import BaseResolver
from barbados.services.logging import LogService
from barbados.objects.resolution import Resolution, DirectResolution, ImplicitResolution, MissingResolution
from barbados.objects.resolution.summary import SpecResolutionSummary
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.indexers.inventoryspec import InventorySpecResolutionIndexer
from barbados.factories.specresolution import SpecResolutionFactory
from barbados.serializers import ObjectSerializer


class RecipeResolver(BaseResolver):
    @classmethod
    def resolve(cls, inventory, cocktail, spec_slug=None):
        """
        Process a Recipe resolution request. This request could be for all specs of a cocktail
        or just one.
        :param inventory: Inventory to resolve against.
        :param cocktail: Cocktail object to resolve.
        :param spec_slug: Optional Slug of the spec to resolve (None means do all of them)
        :return: List of SpecResolutionSummary objects.
        """
        results = []

        # We retrieve the tree here and expand the inventory so that there isn't potential
        # inconsistency between retrieving the tree now vs later. It does mean we have to
        # pass it around to various functions.
        tree = IngredientTreeCache.retrieve()
        inventory.expand(tree=tree)

        LogService.info("Found cocktail specs: %s" % [spec.slug for spec in cocktail.specs])
        for spec in cocktail.specs:
            # Skip any specs that the user didn't ask for with the spec_slug
            # parameter.
            if spec_slug and spec.slug != spec_slug:
                LogService.info("Skipping spec %s because you didn't want it." % spec.slug)
                continue

            # Parse the spec
            results.append(cls._resolve_spec(inventory=inventory, cocktail=cocktail, spec=spec, tree=tree))

        # Return the list of results.
        return results

    @staticmethod
    def _resolve_spec(inventory, cocktail, spec, tree):
        """
        Generate a SpecResolutionSummary object for this particular recipe. Reminder
        that Recipe = Cocktail + Spec.
        :param inventory: The Inventory object to resolve against.
        :param cocktail: The Cocktail object to resolve.
        :param spec: The Spec object that you wanted to resolve.
        :param tree: IngredientTree.
        :return: A SpecResolutionSummary.
        """
        # Components use the ingredient slug as their slug so we can safely
        # assume a 1:1 mapping between them.
        LogService.info("Resolving spec %s" % spec.slug)
        # rs = SpecResolutionSummary(inventory_id=inventory.id, cocktail=cocktail, spec=spec)
        rs = SpecResolutionFactory.from_objects(inventory, cocktail, spec)

        try:
            rs = InventorySpecResolutionIndexer.get(rs.index_id)
        except KeyError:
            LogService.warn("Document %s not found in index. Regenerating..." % rs.index_id)

            # @TODO move this into the SpecResolution object itself?
            for component in list(spec.components):
                if inventory.contains(component.slug):
                    substitutes, resolution_status = RecipeResolver._get_direct_resolution(inventory, component)
                else:
                    substitutes, resolution_status = RecipeResolver._get_nondirect_resolution(inventory, component, tree)

                # Construct the SpecResolution object.
                LogService.info("Resolution for %s::%s::%s is %s" % (cocktail.slug, spec.slug, component.slug, resolution_status.status))
                r = Resolution(slug=component.slug, status=resolution_status, substitutes=substitutes,
                               parents=tree.parents(component.slug))

                # Add the resolution to the summary
                rs.add_component(r)

            # Index and Return
            InventorySpecResolutionIndexer.index(rs)

        return rs

    @staticmethod
    def _get_direct_resolution(inventory, component):
        """
        The spec.component.slug is specifically named in the inventory items.
        :return: Tuple of List of substitutes and DirectResolution
        """
        return inventory.substitutes(component.slug), DirectResolution

    @staticmethod
    def _get_nondirect_resolution(inventory, component, tree):
        """
        Now we're looking at the implied versions of the component. By definition
        all of these will be ImpliedResolution because we've had to change what
        we're looking up as.
        This is called Nondirect because it potentially returns Missing as well.
        :param inventory:
        :param component:
        :return: Tuple of List of substitutes and DirectResolution
        """
        substitutes = []
        for implied_component in tree.implies(component.slug):
            # Test for if the inventory contains the implied component
            # explicitly or implicitly.
            if inventory.contains(implied_component):
                # The inventory explicitly contains this implied component.
                substitutes += inventory.substitutes(implied_component)
            elif inventory.contains(implied_component, implicit=True):
                # The inventory implicitly contains this implied component.
                substitutes += inventory.substitutes(implied_component, implicit=True)
            else:
                # The inventory does not contain this implied component in any way.
                continue

        # We have to de-duplicate the substitutes we just calculated.
        substitutes = list(set(substitutes))

        # By this point if we haven't found any explicit or implicit matches
        # for either the direct component or any of its implications, it's missing.
        # If we have then it's considered implicitly available.
        if substitutes:
            return substitutes, ImplicitResolution

        return [], MissingResolution
