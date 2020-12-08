from barbados.resolvers.baseresolver import BaseResolver
from barbados.services.logging import Log
from barbados.resolution import Resolution, DirectResolution, ImplicitResolution, MissingResolution, SpecResolutionSummary
from barbados.caches import IngredientTreeCache


class RecipeResolver(BaseResolver):
    @classmethod
    def resolve(cls, inventory, cocktail, spec_slug=None):
        results = []

        tree = IngredientTreeCache.retrieve()
        inventory.populate_implicit_items(tree=tree)

        Log.info("Cocktail specs: %s" % [spec.slug for spec in cocktail.specs])
        for spec in cocktail.specs:
            # Skip any specs that the user didn't ask for with the spec_slug
            # parameter.
            if spec_slug and spec.slug != spec_slug:
                Log.info("Skipping slug %s because you didn't want it." % spec.slug)
                continue

            # Parse the spec
            results.append(cls._resolve_spec(inventory=inventory, cocktail=cocktail, spec=spec, tree=tree))

        # Return the list of results.
        return results

    @staticmethod
    def _resolve_spec(inventory, cocktail, spec, tree):
        # Components use the ingredient slug as their slug so we can safely
        # assume a 1:1 mapping between them.
        rs = SpecResolutionSummary(cocktail_slug=cocktail.slug, spec_slug=spec.slug)

        for component in spec.components:
            r = None
            if inventory.contains(component.slug):
                # The spec.component.slug is specifically named in the inventory items.
                r = Resolution(slug=component.slug, status=DirectResolution)
            elif inventory.contains(component.slug, implicit=True):
                # The spec.component.slug is specifically named in the inventory implicit items.
                # Targets "generic" spec components when there are "specific" or "generic"
                # implicit items in the inventory.
                r = Resolution(slug=component.slug, status=ImplicitResolution)
            else:
                # Now we're looking at the implied versions of the component. By definition
                # all of these will be ImpliedResolution because we've had to change what
                # we're looking up as.
                for implied_component in tree.implies(component.slug):
                    if inventory.contains(implied_component) or inventory.contains(implied_component, implicit=True):
                        r = Resolution(slug=component.slug, status=ImplicitResolution)
                        # Stop further processing on this component.
                        break

                # By this point we haven't found any explicit or implicit matches
                # for either the direct component or any of its implications.
                # It's missing.
                if r is None:
                    r = Resolution(slug=component.slug, status=MissingResolution)

            # Add the resolution to the summary
            rs.add_component(r)

        return rs
