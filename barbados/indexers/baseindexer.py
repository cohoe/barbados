class BaseIndexer:
    @classmethod
    def index(cls, obj):
        index = cls.factory.obj_to_index(obj, cls.for_index)
        index.save()

    @property
    def for_class(self):
        raise NotImplementedError()

    @property
    def for_index(self):
        raise NotImplementedError()

    @property
    def factory(self):
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
        index_obj = cls.factory.obj_to_index(obj, cls.index)
        cls.index.delete(index_obj)