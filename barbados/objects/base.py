class BarbadosObject:
    """
    Common object class that any non-operational object must inherit
    from. In general this is anything that gets stored in the various
    data sources (database, indexes, etc).
    Operational objects (indexes, indexers, factories, etc) are not
    meant to be children of this class.
    """
    def serialize(self, serializer):
        raise NotImplementedError

    # @TODO tie this in with the validators to add a .validate() function
    # to the object? That way we don't need to bother importing validators
    # all over the place.
