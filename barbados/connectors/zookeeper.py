import os
from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NoNodeError
from kazoo.retry import KazooRetry
from kazoo.handlers.threading import KazooTimeoutError
from barbados.exceptions import FatalException
from barbados.services.logging import LogService


class ZookeeperConnector:
    """
    Apache ZooKeeper distributed data store connector. Since this is used as the source
    of everything in this application it cannot rely on the barbados.settings.Setting class.
    Using it here would be a dependency loop.
    """
    def __init__(self, hosts=os.getenv('AMARI_ZOOKEEPER_HOSTS', '127.0.0.1:2181'), read_only=False):
        self.hosts = hosts
        self.read_only = read_only

        LogService.info("Using Zookeeper hosts: \"%s\"" % hosts)

    def set(self, path, value):
        """
        Set a given key in the configuration store to a value. This
        will create the key if it does not exist.
        :param path: Normalized path in the hierarchy to the key.
        :param value: String of the value to set
        :return: None or Exception
        """
        self._connect()
        self.zk.ensure_path(path)

        if not self.zk.exists:
            self.zk.create(path, str.encode(value))
        else:
            self.zk.set(path, str.encode(value))

    def get(self, path):
        """
        Fetch the value from the configuration store for the given key.
        :param path: Normalized path in the hierarchy to the key.
        :return: str or Exception
        """
        self._connect()
        try:
            data, stat = self.zk.get(path)
            return data.decode("utf-8")
        except NoNodeError:
            raise KeyError("%s does not exist." % path)
        except Exception as e:
            LogService.error(e.__class__)
            LogService.error(e)

    def _connect(self):
        """
        [re]Connect to the ZooKeeper host(s). Create a local attribute to this class
        that acts as the client and does the actual interactions with ZK.
        :return: None
        """
        # If we don't have a self.zk attribute then we've never connected.
        if not hasattr(self, 'zk'):
            self.zk = KazooClient(hosts=self.hosts, read_only=self.read_only, timeout=5, connection_retry=self._get_retry())
        # Any state not connected is a bad thing. Warn and continue with execution below.
        elif self.zk.state != KazooState.CONNECTED:
            LogService.warning("ZooKeeper state is %s" % self.zk.state)
            pass
        # Connected state is good. Do nothing.
        elif self.zk.state == KazooState.CONNECTED:
            return
        # I'm not sure if this actually does anything...
        else:
            raise Exception("We in a weird state. %s" % self.zk.state)

        # Start the connection now that it's guaranteed to exist.
        try:
            return self.zk.start()
        except KazooTimeoutError as e:
            raise FatalException("Timeout connecting to ZooKeeper (%s)" % e)

    @staticmethod
    def _get_retry():
        """
        ZooKeeper connection retry is weird and needs a particular object to achieve.
        Create that object with its appropriate settings here and return it.
        :return: KazooRetry object.
        """
        return KazooRetry(max_tries=5, backoff=2, max_delay=30)
