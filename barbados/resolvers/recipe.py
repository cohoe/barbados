from barbados.resolvers.base import BaseResolver
from barbados.services.logging import LogService
from barbados.objects.resolution import Resolution, DirectResolution, ImplicitResolution, MissingResolution
from barbados.objects.resolution.summary import SpecResolutionSummary
from barbados.caches.ingredienttree import IngredientTreeCache
from barbados.indexers.inventoryspec import InventorySpecResolutionIndexer


class RecipeResolver(BaseResolver):
    @classmethod
    def resolve(cls, inventory, cocktail, spec_slug=None):
        results = []

        tree = IngredientTreeCache.retrieve()
        inventory.expand(tree=tree)

        LogService.info("Cocktail specs: %s" % [spec.slug for spec in cocktail.specs])
        for spec in cocktail.specs:
            # Skip any specs that the user didn't ask for with the spec_slug
            # parameter.
            if spec_slug and spec.slug != spec_slug:
                LogService.info("Skipping slug %s because you didn't want it." % spec.slug)
                continue

            # Parse the spec
            results.append(cls._resolve_spec(inventory=inventory, cocktail=cocktail, spec=spec, tree=tree))

        # Return the list of results.
        return results

    @staticmethod
    def _resolve_spec(inventory, cocktail, spec, tree):
        # Components use the ingredient slug as their slug so we can safely
        # assume a 1:1 mapping between them.
        rs = SpecResolutionSummary(inventory_id=inventory.id, cocktail=cocktail, spec=spec)

        for component in spec.components:
            r = None
            if inventory.contains(component.slug):
                # The spec.component.slug is specifically named in the inventory items.
                substitutes = inventory.substitutes(component.slug)
                r = Resolution(slug=component.slug, status=DirectResolution, substitutes=substitutes)
            elif inventory.contains(component.slug, implicit=True):
                # The spec.component.slug is specifically named in the inventory implicit items.
                # Targets "generic" spec components when there are "specific" or "generic"
                # implicit items in the inventory.
                substitutes = inventory.substitutes(component.slug, implicit=True)
                r = Resolution(slug=component.slug, status=ImplicitResolution, substitutes=substitutes)
            else:
                # Now we're looking at the implied versions of the component. By definition
                # all of these will be ImpliedResolution because we've had to change what
                # we're looking up as.
                for implied_component in tree.implies(component.slug):
                    # Test for if the inventory contains the implied component
                    # explicitly or implicitly.
                    # Stop further processing on this component if it does.
                    if inventory.contains(implied_component):
                        # The inventory explicitly contains this implied component
                        substitutes = inventory.substitutes(implied_component)
                        r = Resolution(slug=component.slug, status=ImplicitResolution, substitutes=substitutes)
                        break
                    elif inventory.contains(implied_component, implicit=True):
                        # The inventory implicitly  contains this implied component
                        substitutes = inventory.substitutes(implied_component, implicit=True)
                        r = Resolution(slug=component.slug, status=ImplicitResolution, substitutes=substitutes)
                        break
                # By this point we haven't found any explicit or implicit matches
                # for either the direct component or any of its implications.
                # It's missing.
                if r is None:
                    r = Resolution(slug=component.slug, status=MissingResolution)

            # Fill in the parent and parents of the component.
            # r.parent = tree.parent(r.slug).tag # @TODO is this actually needed anymore? I don't think so.
            r.parents = tree.parents(r.slug)

            # Add the resolution to the summary
            rs.add_component(r)

        # Index
        # indexer_factory.get_indexer(rs).index(rs)
        InventorySpecResolutionIndexer.index(rs)

        return rs
