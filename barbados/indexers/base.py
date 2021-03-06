class BaseIndexer:
    """
    Template interface class for any Indexers.
    """
    @classmethod
    def index(cls, obj):
        """
        Store the object in the index.
        :param obj: barbados.objects.base.BarbadosObject child.
        :return: None
        """
        index = cls.factory.obj_to_index(obj, cls.for_index)
        index.save()

    @property
    def for_class(self):
        """
        Parameter containing the class that this indexer is to be used for.
        :return: barbados.objects.base.BarbadosObject child class.
        """
        raise NotImplementedError()

    @property
    def for_index(self):
        """
        Parameter containing the index class that this indexer corresponds to.
        :return: barbados.indexes.base.BaseIndex child class.
        """
        raise NotImplementedError()

    @property
    def factory(self):
        """
        Parameter containing the factory that is used to turn the object into an
        index instance.
        :return: barbados.factories.base.BaseFactory child class.
        """
        raise NotImplementedError()

    @classmethod
    def reindex(cls, session):
        """
        Regenerate the data in an index from the database.
        :param session: Database session context.
        :return: Number of objects indexed.
        """
        # Delete all data in the index.
        cls.empty()

        # Re-populate the index based on the data from the database.
        objects = cls.factory.produce_all_objs(session=session)
        for obj in objects:
            cls.index(obj)

        return len(objects)

    @classmethod
    def empty(cls):
        """
        Delete all records within an index.
        :return: None
        """
        cls.for_index.delete_all()

    @classmethod
    def delete(cls, obj):
        """
        Delete a specific object from its index.
        :param obj: barbados.objects.base.BarbadosObject child instance.
        :return: None
        """
        index_obj = cls.factory.obj_to_index(obj, cls.index)
        cls.index.delete(index_obj)
