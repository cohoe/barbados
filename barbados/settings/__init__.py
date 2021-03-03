import os
from barbados.services.registry import RegistryService


class Setting:
    """
    Standard class for accessing a setting provided either by the registry,
    environment variable, and defaults.
    """
    def __init__(self, path, default, env=None, type_=None):
        self.path = path
        self.env = env
        self.default = default
        self.type_ = type_

    def get_value(self, skip_registry=False):
        """
        Retrieve the value of a setting from the various sources.
        Order goes: Registry, Environment Variable, Default.
        This potentially enforces a type as well.
        :param skip_registry: Boolean to skip looking at the registry.
        :return: Value of the setting.
        """
        try:
            if skip_registry:
                raise KeyError
            value = RegistryService.get(self.path)
        except KeyError:
            value = os.getenv(key=self.env, default=self.default) if self.env else self.default

        if self.type_ and not isinstance(value, self.type_) and value is not None:
            value = self.type_(value)

        return value

    def __repr__(self):
        return "Barbados::Settings::Setting[%s]" % self.path
