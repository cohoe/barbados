from barbados.connectors import ZookeeperConnector
from barbados.connectors import PostgresqlConnector


class Registry:
    """
    Generic registry service class. This exists to provide a common interface
    to the connectors. Potential connectors could be:
    * Zookeeper
    * AWS SSM Parameter Store
    * etcd
    """

    registry_connector = ZookeeperConnector()

    @staticmethod
    def get(path):
        """
        Fetch the value from the configuration store for the given key.
        :param path: Normalized path in the hierarchy to the key.
        :return: str or Exception
        """
        return Registry.registry_connector.get(path)

    @staticmethod
    def set(path, value):
        """
        Set a given key in the configuration store to a value. This
        will create the key if it does not exist.
        :param path: Normalized path in the hierarchy to the key.
        :param value: String of the value to set
        :return: None or Exception
        """
        return Registry.registry_connector.set(path, value)

    @staticmethod
    def get_database_connection():
        """
        @TODO I don't like this is here but until a better place
        presents itself its good enough.
        :return:
        """
        db_database = Registry.get('/database/postgres/database')
        db_username = Registry.get('/database/postgres/username')
        db_password = Registry.get('/database/postgres/password')

        return PostgresqlConnector(database=db_database, username=db_username, password=db_password)