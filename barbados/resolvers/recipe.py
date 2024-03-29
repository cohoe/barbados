from barbados.resolvers.base import BaseResolver
from barbados.services.logging import LogService
from barbados.objects.resolution.status import DirectResolutionStatus, ImplicitResolutionStatus, MissingResolutionStatus
from barbados.objects.resolution.component import ComponentResolution
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.factories.reciperesolution import RecipeResolutionFactory
from barbados.exceptions import FactoryException


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

        LogService.info("Cocktail %s has specs: %s" % (cocktail.slug, [spec.slug for spec in cocktail.specs]))
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
        Generate a RecipeResolutionSummary object for this particular recipe. Reminder
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
        rs = RecipeResolutionFactory.from_objects(inventory, cocktail, spec)
        try:
            rs = RecipeResolutionFactory.produce_obj(id=rs.id)
            LogService.info("Found resolution %s in the database" % rs.id)
        except KeyError:
            LogService.warn("Document %s not found in database. Regenerating..." % rs.id)
            rs = RecipeResolver._populate_components(summary=rs, cocktail=cocktail, spec=spec, inventory=inventory, tree=tree)

        return rs

    @staticmethod
    def _populate_components(summary, cocktail, spec, inventory, tree):
        """
        Fill in the components of a RecipeResolutionSummary.
        :param summary: RecipeResolutionSummary object.
        :param cocktail: Cocktail object.
        :param spec: Spec object.
        :param inventory: Inventory object.
        :param tree: IngredientTree object. This is loaded elsewhere to prevent over-loading.
        :return: RecipeResolutionSummary.
        """
        # Just in case we were given a populated object, blow away the components.
        summary.components = []

        # Go through all of them.
        for component in list(spec.components):
            if inventory.contains(component.slug):
                substitutes, resolution_status = RecipeResolver._get_direct_resolution(inventory, component)
            else:
                substitutes, resolution_status = RecipeResolver._get_nondirect_resolution(inventory, component, tree)

                # Construct the SpecResolution object.
            LogService.info("Resolution for %s::%s::%s is %s" % (cocktail.slug, spec.slug, component.slug, resolution_status.status))
            r = ComponentResolution(slug=component.slug, status=resolution_status, substitutes=substitutes,
                                    parents=tree.parents(component.slug))

            # Add the resolution to the summary
            summary.add_component(r)

        # Done
        return summary

    @staticmethod
    def _get_direct_resolution(inventory, component):
        """
        The spec.component.slug is specifically named in the inventory items.
        :return: Tuple of List of substitutes and DirectResolution
        """
        return inventory.substitutes(component.slug), DirectResolutionStatus

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
            return substitutes, ImplicitResolutionStatus

        return [], MissingResolutionStatus
