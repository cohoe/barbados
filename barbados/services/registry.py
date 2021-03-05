from barbados.connectors.zookeeper import ZookeeperConnector


class RegistryService:
    """
    Generic registry service class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * Zookeeper
    * AWS SSM Parameter Store
    * etcd
    """

    connector = ZookeeperConnector()

    @staticmethod
    def get(path, default_none=False):
        """
        Fetch the value from the configuration store for the given key.
        :param path: Normalized path in the hierarchy to the key.
        :param default_none: Boolean of whether to return None instead of a KeyError if it doesn't exist.
        :return: str or Exception
        """
        try:
            return RegistryService.connector.get(path)
        except KeyError as e:
            if not default_none:
                raise e

    @staticmethod
    def set(path, value):
        """
        Set a given key in the configuration store to a value. This
        will create the key if it does not exist.
        :param path: Normalized path in the hierarchy to the key.
        :param value: String of the value to set
        :return: None or Exception
        """
        return RegistryService.connector.set(path, value)
