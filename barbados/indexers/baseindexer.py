class BaseIndexer:
    @staticmethod
    def index(*args, **kwargs):
        raise NotImplementedError()

    @property
    def for_class(self):
        raise NotImplementedError()
