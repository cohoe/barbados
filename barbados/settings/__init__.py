import os
from barbados.services.registry import RegistryService


class Setting:
    """
    Standard class for accessing a setting provided either by the registry,
    environment variable, and defaults.
    @TODO support a config file?
    """
    def __init__(self, path, env, default, type_=None):
        self.path = path
        self.env = env
        self.default = default
        self.type_ = type_

    def get_value(self):
        """
        Retrieve the value of a setting from the various sources.
        Order goes: Registry, Environment Variable, Default.
        This potentially enforces a type as well.
        :return: Value of the setting.
        """
        try:
            value = RegistryService.get(self.path)
        except KeyError:
            value = os.getenv(key=self.env, default=self.default)

        if self.type_ and not isinstance(value, self.type_):
            value = self.type_(value)

        return value

    def __repr__(self):
        return "Barbados::Settings::Setting[%s]" % self.path
