import os
from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NoNodeError
from kazoo.retry import KazooRetry
from kazoo.handlers.threading import KazooTimeoutError
from barbados.exceptions import FatalException
from barbados.services.logging import Log


class ZookeeperConnector:
    def __init__(self, hosts=os.getenv('ZOOKEEPER_HOSTS', '127.0.0.1:2181'), read_only=False):
        self.hosts = hosts
        self.read_only = read_only

        Log.info("Using Zookeeper hosts: \"%s\"" % hosts)

    def set(self, path, value):
        self._connect()
        self.zk.ensure_path(path)

        if not self.zk.exists:
            self.zk.create(path, str.encode(value))
        else:
            self.zk.set(path, str.encode(value))

    def get(self, path):
        self._connect()
        try:
            data, stat = self.zk.get(path)
            return data.decode("utf-8")
        except NoNodeError:
            raise KeyError("%s does not exist." % path)
        except Exception as e:
            Log.error(e.__class__)
            Log.error(e)

    def _connect(self):
        if not hasattr(self, 'zk'):
            self.zk = KazooClient(hosts=self.hosts, read_only=self.read_only, timeout=5, connection_retry=self._get_retry())
        elif self.zk.state != KazooState.CONNECTED:
            pass
        elif self.zk.state == KazooState.CONNECTED:
            return
        else:
            raise Exception("We in a weird state. %s" % self.zk.state)

        try:
            return self.zk.start()
        except KazooTimeoutError as e:
            raise FatalException("Timeout connecting to ZooKeeper (%s)" % e)

    @staticmethod
    def _get_retry():
        return KazooRetry(max_tries=5, backoff=2)
