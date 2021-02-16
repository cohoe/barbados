class BaseMetric:
    key = NotImplementedError
    instance = 'all'

    @classmethod
    def collect(cls, *args, **kwargs):
        raise NotImplementedError
