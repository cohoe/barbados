from barbados.exceptions import NotFoundError, SearchException
from barbados.services.logging import LogService


class BaseIndexer:
    """
    Template interface class for any Indexers.
    """
    @classmethod
    def index(cls, obj):
        """
        Store the object in the index.
        @TODO rebrand to .put()?
        :param obj: barbados.objects.base.BarbadosObject child.
        :return: None
        """
        index = cls.factory.obj_to_index(obj)
        index.save()

    @classmethod
    def get(cls, id):
        """
        Retrieve an object from the index.
        :param id: ElasticSearch document ID
        :return: BarbadosObject child.
        """
        try:
            index = cls.for_index.get(id)
            return cls.factory.index_to_obj(index)
        except NotFoundError:
            raise KeyError("Document %s not found in Index %s" % (id, cls.for_index.Index.name))

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
    def delete(cls, obj, fatal=False):
        """
        Delete a specific object from its index.
        Fatal changed to implicitly be false since if something isn't
        in the index (kinda problematic?) whatevs thats the desired state.
        :param obj: barbados.objects.base.BarbadosObject child instance.
        :param fatal: Should not being in the index be a critical problem.
        :return: None
        """
        index_obj = cls.factory.obj_to_index(obj)

        try:
            cls.for_index.delete(index_obj)
        except NotFoundError as e:
            if fatal:
                raise SearchException(e)
            LogService.warn("Object %s was not found in index on DELETE. This probably isn't a problem?" % obj)
