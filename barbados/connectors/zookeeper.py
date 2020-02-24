import logging
from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NoNodeError


class ZookeeperConnector:
    def __init__(self, hosts='127.0.0.1:2181', read_only=False):
        self.hosts = hosts
        self.read_only = read_only

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
            logging.error(e.__class__)
            logging.error(e)

    def _connect(self):
        if not hasattr(self, 'zk'):
            self.zk = KazooClient(hosts=self.hosts, read_only=self.read_only)
            return self.zk.start()
        elif self.zk.state != KazooState.CONNECTED:
            return self.zk.start()
        elif self.zk.state == KazooState.CONNECTED:
            return
        else:
            raise Exception("We in a weird state. %s" % self.zk.state)
