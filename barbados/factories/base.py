import copy
from barbados.serializers import ObjectSerializer
from barbados.services.logging import LogService
from barbados.services.database import DatabaseService


class BaseFactory:

    # @TODO I'm pretty sure this isn't manifesting how I expected it to.
    # It still shits an error so that's good.
    @property
    def _model(self):
        raise NotImplementedError()

    @property
    def _validator(self):
        raise NotImplementedError()

    @staticmethod
    def obj_to_index(obj, index_class, format='dict'):
        """
        Serialize an object into a standard form suitable
        for indexing.
        :param obj: Serializable object.
        :param index_class: The ElasticSearch DSL class representing the intended index.
        :param format: Format of the data to pass to the serializer.
        :return: Instance of the Index class.
        """
        # I really hope I don't regret this. id and slug could be problematic.
        try:
            id = getattr(obj, 'id')
        except AttributeError:
            id = getattr(obj, 'slug')

        return index_class(meta={'id': id}, **ObjectSerializer.serialize(obj, format))

    @classmethod
    def model_to_obj(cls, model):
        """
        This exists to ensure common functionality with CocktailModel.
        Convert a Model into an Object. There is some SQLAlchemy crap that must
        be removed in order to basically dump the model's dictionary
        into the raw_to_obj() function.
        :param model: barbados.models.BarbadosModel child.
        :return: A barbados.objects.* object instance.
        """
        # Deepcopy is needed to prevent the pop() from affecting
        # the actual model used in-memory by Jamaica.
        # Smells like sqlalchemy.orm.exc.UnmappedInstanceError
        # "but this instance lacks instrumentation"
        try:
            model_dict = copy.deepcopy(model.__dict__)
            model_dict.pop('_sa_instance_state')
        except AttributeError:
            raise KeyError("Object not found")

        return cls.raw_to_obj(model_dict)

    @classmethod
    def obj_to_model(cls, obj):
        return cls._model(**ObjectSerializer.serialize(obj, 'dict'))

    @staticmethod
    def raw_to_obj(raw):
        raise NotImplementedError

    @staticmethod
    def required_keys():
        raise NotImplementedError

    @staticmethod
    def sanitize_raw(raw_input, required_keys):
        """
        Forces the default value of certain required attributes to their expected defaults.
        :param raw_input: Dictionary
        :param required_keys: Dictionary of keys and their data expected data type.
        :return: sanitized raw_input (dict)
        """
        for key in required_keys.keys():
            # If the required key is not in the input, set it to the default.
            if key not in raw_input.keys():
                raw_input[key] = required_keys[key]
            # If the required key should be a list and in the input it is not, force
            # it to an empty list.
            if type(required_keys[key]) is list:
                if raw_input[key] is None:
                    raw_input[key] = required_keys[key]

        return raw_input

    @classmethod
    def produce_obj(cls, id):
        """
        Produce an appropriate object from the factory.
        :param id: ID parameter of the record to lookup
        :return: Object from the Model.
        """
        with DatabaseService.get_session() as current_session:
            result = current_session.query(cls._model).get(id)
            if not result:
                raise KeyError('Not found')
            obj = cls.model_to_obj(result)

        return obj

    @classmethod
    def produce_all_objs(cls):
        """
        Produce a list of appropriate objects from this factory.
        :param session: Database Session context.
        :return:
        """
        with DatabaseService.get_session() as session:
            results = session.query(cls._model).all()

            objects = []
            for result in results:
                obj = cls.model_to_obj(result)
                objects.append(obj)

        return objects

    @classmethod
    def store_obj(cls, obj):
        """
        Store an object in the database.
        :param session: Database Session context.
        :param obj: The object to store.
        :return: Model corresponding to the object.
        """
        # model = cls._model(**ObjectSerializer.serialize(obj, 'dict'))
        with DatabaseService.get_session() as session:
            model = cls.obj_to_model(obj)

            # Validate it.
            cls._validator(model).validate(session=session)

            # Save it to the database.
            session.add(model)
            session.commit()

    @classmethod
    def delete_obj(cls, obj, commit=True, id_attr='slug'):
        """
        Delete an object from the database.
        :param obj: The object to delete.
        :param commit: Whether to commit this transaction now or deal with it yourself. Useful for batches.
        :return: Model corresponding to the object that was deleted.
        """
        try:
            id = obj.slug
        except AttributeError:
            id = obj.id

        with DatabaseService.get_session() as session:
            model = session.query(cls._model).get(id)

            if not model:
                raise KeyError("Model for %s not found" % id)

            # Delete it from the database.
            session.delete(model)
            if commit:
                session.commit()

    @classmethod
    def update_obj(cls, obj, commit=True):
        """
        Update an existing model based on its current object state.
        :param obj: The object to delete.
        :param commit: Whether to commit this transaction now or deal with it yourself. Useful for batches.
        :return: New model.
        """
        # @TODO this is unsafe based on if the slug/id changes. Maybe I gotta enforce that?
        with DatabaseService.get_session() as session:
            model = session.query(cls._model).get(obj.slug)

            # This feels unsafe, but should be OK.
            # https://stackoverflow.com/questions/9667138/how-to-update-sqlalchemy-row-entry
            for key, value in ObjectSerializer.serialize(obj, 'dict').items():
                old_value = getattr(model, key)
                setattr(model, key, value)

                if old_value != value:
                    LogService.info("Updating %s: '%s'->'%s'" % (key, old_value, value))

            if commit:
                session.commit()

            return model
