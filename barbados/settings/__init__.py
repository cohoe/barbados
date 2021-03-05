import os
from barbados.services.registry import RegistryService
from barbados.exceptions import SettingsException
from barbados.services.logging import LogService


class Setting:
    """
    Standard class for accessing a setting provided either by the registry,
    environment variable, and defaults.
    """

    def __init__(self, path, type_, default=None, env=''):
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
        registry_value = RegistryService.get(self.path, default_none=True)
        env_value = os.getenv(key=self.env, default=None)
        default_value = self.default

        potential_values = (registry_value, env_value, default_value)
        if skip_registry:
            potential_values = (env_value, default_value)

        # https://stackoverflow.com/questions/18533620/getting-the-first-non-none-value-from-list
        try:
            setting_value = next(value for value in potential_values if value is not None)
        except StopIteration:
            raise SettingsException("No valid setting found for %s" % self.path)

        LogService.info("Setting %s => %s" % (self.path, setting_value))
        return setting_value

    def __repr__(self):
        return "Barbados::Settings::Setting[%s=%s]" % (self.path, self.get_value())
